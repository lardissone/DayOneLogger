import os
import base64
import requests
import arrow

from . import Service


# enter you WakaTime API key or set it in your environment vars
WAKATIME_API_KEY = os.environ.get(
    'WAKATIME_API_KEY',
    '(enter here your key if not using environment variable)'
)


class wakatime(Service):

    service = 'wakatime'

    def _get_data(self, day):
        url = 'https://wakatime.com/api/v1/summary/daily?start=%s&end=%s' % (
            day.format('YYYY/MM/DD'),
            day.format('YYYY/MM/DD')
        )

        key = bytes.decode(base64.b64encode(str.encode(WAKATIME_API_KEY)))
        r = requests.get(
            url,
            headers={'Authorization': 'Basic %s' % key}
        )

        if not r.status_code == 200:
            return False

        return r.json()


    def parse(self):
        start_date = arrow.get(self.last_sync)
        end_date = arrow.now().replace(
            days=-1,
            hour=23,
            minute=59,
            second=59)

        diff = end_date - start_date
        days = diff.days if diff.days <= 7 else 7

        s = start_date
        entries = []
        for i in range(0, days):
            response = self._get_data(s.replace(days=i + 1))
            if response and response['data']:
                if response['data'][0]['languages']:
                    entries.append({
                        'service': self.service,
                        'date': s.replace(days=i),
                        'values': response['data'][0]
                    })

        text = 'Today total time: %(total)s\n\n'
        text += '**Projects**\n%(projects)s\n\n'
        text += '**Languages**\n%(languages)s\n'

        for e in entries:
            projects = []
            for p in e['values']['projects']:
                projects.append(
                    '- %s: %s' % (
                        p['name'],
                        p['text']
                    )
                )

            languages = []
            for l in e['values']['languages']:
                languages.append(
                    '- %s: %s%%' % (
                        l['name'],
                        l['percent']
                    )
                )

            e['md'] = text % {
                'total': e['values']['grand_total']['text'],
                'projects': '\n'.join(projects),
                'languages': '\n'.join(languages)
            }

        return entries
