from . import Service


class tweets(Service):

    service = 'tweets'

    def parse(self):
        parts = self.process_file('tweets.txt')
        entries = self.get_entries(self.service, parts)

        for e in entries:
            link = e['values'][1].strip() if len(e['values']) > 1 else ''

            e['md'] = '- %s: %s - %s' % (
                e['date'].format('HH:mm'),
                self._md_escape(e['values'][0].strip()),
                self._md_link(link),
            )
        return entries
