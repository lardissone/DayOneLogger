#!/usr/bin/env python
"""
DayOneLogger - Log anything you add to a folder to Day One
Author: Leandro Ardissone <leandro@ardissone.com>
More Info: https://github.com/lardissone/DayOneLogger
"""

import os
import sys
import uuid
import plistlib
import platform
import arrow

from utils import get_dropbox_path, get_icloud_path
import services as sources

# Settings -------
IFTTT_DIR = os.path.expanduser('~/Dropbox/IFTTT/DayOneLogger')
# Dropbox:
DAYONE_DIR = get_dropbox_path()
# iCloud:
# DAYONE_DIR = get_icloud_path()

SERVICES = [
    'github',
    'reminders',
    'tweets',
    'movies',
    'places',
    'tracks',
    'wakatime',
    'todoist'
]

# TODO: find a way to get `tzlocal` working on OSX to get these values
TIME_ZONE = 'America/Argentina/Buenos_Aires'
TIME_ZONE_OFFSET = 3
ENTRY_TAGS = ['daily']
# ----------------

DEBUG = False  # if True, it doesn't writes to Day One

LOCAL_PATH = os.path.dirname(os.path.realpath(__file__))
SYNC_FILE = os.path.join(LOCAL_PATH, '.last_sync')

try:
    if not DEBUG:
        with open(SYNC_FILE) as f:
            LAST_SYNC = f.read()
    else:
        LAST_SYNC = str(arrow.now().replace(weeks=-1))
except IOError:
    LAST_SYNC = str(arrow.get('2001-01-01').datetime)


class DayOneLogger(object):
    data = {
        'days': [],
        'entries': {}
    }
    services_titles = {
        'places': '### Places',
        'github': '### Github',
        'reminders': '### Reminders',
        'movies': '### Movies',
        'tracks': '### Loved tracks',
        'tweets': '### Tweets',
        'wakatime': '### Coding stats',
        'todoist': '### Todoist completed tasks',
    }
    services_used = []

    def __init__(self, last_sync):
        self.last_sync = arrow.get(last_sync).datetime

    def _group_by_day(self, entries):
        for e in entries:
            day = e['date'].date()
            if day not in self.data['days']:
                self.data['days'].append(day)
                self.data['entries'][day] = {}

            if not e['service'] in self.data['entries'][day]:
                self.data['entries'][day][e['service']] = []
            self.data['entries'][day][e['service']].append(e)

    def _generate_markdown(self):
        """ Generates a single markdown output for all entries """

        self.data['md'] = {}

        for day in sorted(self.data['days']):

            if day in self.data['entries']:
                title = '# Things done on %s'
                md = [title % arrow.get(day).format('MMMM DD, YYYY')]

                entries = self.data['entries'][day]

                for service in self.services_used:
                    if service in entries:
                        md += ['', self.services_titles[service]]

                        sorted_list = sorted(
                            entries[service], key=lambda k: k['date']
                        )
                        md += [m['md'] for m in sorted_list]

                md += [''] * 2

                self.data['md'][day] = '\n'.join(x.decode('utf-8') for x in md)

    def _save_to_day_one(self):
        for day in sorted(self.data['days'])[:-1]:
        #for day in sorted(self.data['days']):

            uuid_val = uuid.uuid1().hex.upper()
            utc_time = arrow.utcnow()
            filename = os.path.join(DAYONE_DIR, uuid_val + ".doentry")

            now = arrow.now()
            entry_date = arrow.get(day)
            entry_date = entry_date.replace(hour=now.hour, minute=now.minute)
            entry_date = entry_date.replace(hours=TIME_ZONE_OFFSET).datetime

            entry_plist = {
                'Creation Date': entry_date,
                'Starred': False,
                'Entry Text': self.data['md'][day],
                'Time Zone': TIME_ZONE,
                'UUID': uuid_val,
                'Tags': ENTRY_TAGS,
                'Creator': {
                    'Device Agent': platform.uname()[0],
                    'Generation Date': utc_time.datetime,
                    'Host Name': platform.node(),
                    'OS Agent': platform.platform(),
                    'Software Agent': 'DayOneLogger'
                }
            }
            if not DEBUG:
                plistlib.writePlist(entry_plist, filename)

    def process(self, services, markdown=True, save=True):
        entries = []
        self.services_used = services
        for service in services:
            source = __import__('services.%s' % service)
            source = getattr(sources, service)
            s = getattr(source, service)(IFTTT_DIR, LAST_SYNC, DEBUG)
            entries += s.parse()

        if not entries:
            print 'nothing to process this time...'
            sys.exit()

        self._group_by_day(entries)

        if markdown:
            self._generate_markdown()

        if save:
            self._save_to_day_one()

        last_entry = arrow.now().replace(
            days=-1,
            hour=23,
            minute=59,
            second=59)

        if not DEBUG:
            with open(SYNC_FILE, 'w') as f:
                f.write(str(last_entry.datetime))


if __name__ == '__main__':
    do = DayOneLogger(LAST_SYNC)
    do.process(SERVICES)
