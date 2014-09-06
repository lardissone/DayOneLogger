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


def get_icloud_path():
    mobile_docs = os.path.expanduser('~/Library/Mobile Documents')
    dayone_path = [s for s in os.listdir(mobile_docs) if 'dayoneapp' in s]

    if not dayone_path:
        print 'Error: Day One not syncing to iCloud'
        sys.exit()

    return '%s/%s/Documents/Journal_dayone/entries/' % (
        mobile_docs,
        dayone_path[0])

def get_dropbox_path():
    return os.path.expanduser('~/Dropbox/Apps/Day One/Journal.dayone/entries')

# Settings -------
IFTTT_DIR = os.path.expanduser('~/Dropbox/IFTTT/DayOneLogger')
# Dropbox:
DAYONE_DIR = get_dropbox_path()
# iCloud:
# DAYONE_DIR = get_icloud_path()

# TODO: find a way to get `tzlocal` working on OSX to get these values
TIME_ZONE = 'America/Argentina/Buenos_Aires'
TIME_ZONE_OFFSET = 3
ENTRY_TAGS = ['daily',]

# ----------------

try:
    with open('.last_sync') as f:
        LAST_SYNC = f.read()
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
        'tweets': '### Tweets'
    }
    services_used = []


    def __init__(self, iftttdir, last_sync):
        self.iftttdir = iftttdir
        self.last_sync = arrow.get(last_sync).datetime

    def _open_file(self, filename):
        filename = '%s/%s' % (self.iftttdir, filename)
        return open(filename).read().split('@done')[:-1]

    def _get_entries(self, service, parts):
        entries = []
        for n in parts:
            p = n.lstrip().split('|~|')
            day = arrow.get(p[0], 'MMMM DD, YYYY at HH:mmA')

            if day.datetime > self.last_sync:
                entries.append({
                    'service': service,
                    'date': day,
                    'values': p[1:]
                    })
        return entries

    def _group_by_day(self, entries):
        for e in entries:
            day = e['date'].date()
            if day not in self.data['days']:
                self.data['days'].append(day)
                self.data['entries'][day] = {}

            if not e['service'] in self.data['entries'][day]:
                self.data['entries'][day][e['service']] = []
            self.data['entries'][day][e['service']].append(e)

    def _md_link(self, text):
        return '[%s](%s)' % (text, text)

    def _md_escape(self, text):
        escapables = [
            '\\', '`', '*', '_', '{', '}',
            '[', ']', '(', ')', '>', '#', '.',
            '!', '+', '-']
        for char in escapables:
            text = text.replace(char, '\%s' % char)
        return text

    def _generate_markdown(self):
        """ Generates a single markdown output for all entries """

        self.data['md'] = {}

        for day in sorted(self.data['days']):

            if day in self.data['entries']:
                md = ['# Things done on %s' % arrow.get(day).format('MMMM DD, YYYY')]

                entries = self.data['entries'][day]

                for service in self.services_used:
                    if service in entries:
                        md += ['', self.services_titles[service]]

                        sorted_list = sorted(entries[service], key=lambda k: k['date'])
                        md += [m['md'] for m in sorted_list]

                md += [''] * 2

                self.data['md'][day] = '\n'.join(x.decode('utf-8') for x in md)

    def _save_to_day_one(self):
        for day in sorted(self.data['days'])[:-1]:

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
            plistlib.writePlist(entry_plist, filename)

    def process(self, services, markdown=True, save=True):
        entries = []
        self.services_used = services
        for service in services:
            entries += getattr(self, service)(service)

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

        with open('.last_sync', 'w') as f:
            f.write(str(last_entry.datetime))


    # parsers
    def github(self, service, filename='github.txt'):
        parts = self._open_file(filename)
        entries = self._get_entries(service, parts)
        for e in entries:
            e['md'] = '- %s: %s' % (
                e['date'].format('HH:mm'),
                e['values'][0].strip()
            )
        return entries

    def reminders(self, service, filename='reminders.txt'):
        parts = self._open_file(filename)
        entries = self._get_entries(service, parts)
        for e in entries:
            text = e['values'][1].strip()
            if len(e['values']) > 2:
                note = e['values'][2].strip()
                notes = [(' ' * 8) + ('%s' % n) for n in note.split('\n')]
                text += '\n' + '\n'.join(notes)
            e['md'] = '- %s: [%s] %s' % (
                e['date'].format('HH:mm'),
                e['values'][0].strip(),
                text
            )
        return entries

    def movies(self, service, filename='movies.txt'):
        parts = self._open_file(filename)
        entries = self._get_entries(service, parts)
        for e in entries:
            e['md'] = '- %s: **%s**: %s' % (
                e['date'].format('HH:mm'),
                e['values'][0].strip(),
                e['values'][1].replace('lardissone', '').strip(),
            )
        return entries

    def places(self, service, filename='places.txt'):
        parts = self._open_file(filename)
        entries = self._get_entries(service, parts)
        # TODO: add venue URL
        for e in entries:
            map_img = (' ' * 8) + ('![](%s)' % e['values'][1])
            e['md'] = '- %s: **%s**\n%s' % (
                e['date'].format('HH:mm'),
                e['values'][0].strip(),
                map_img
            )
        return entries

    def tracks(self, service, filename='tracks.txt'):
        parts = self._open_file(filename)
        entries = self._get_entries(service, parts)
        for e in entries:
            e['md'] = '- %s: *%s* by **%s**' % (
                e['date'].format('HH:mm'),
                e['values'][0].strip(),
                e['values'][1].strip(),
            )
        return entries

    def tweets(self, service, filename='tweets.txt'):
        parts = self._open_file(filename)
        entries = self._get_entries(service, parts)
        for e in entries:
            e['md'] = '- %s: %s - %s' % (
                e['date'].format('HH:mm'),
                self._md_escape(e['values'][0].strip()),
                self._md_link(e['values'][1].strip()),
            )
        return entries


if __name__ == '__main__':
    do = DayOneLogger(IFTTT_DIR, LAST_SYNC)
    do.process([
        'github',
        'reminders',
        'tweets',
        'movies',
        'places',
        'tracks',])
