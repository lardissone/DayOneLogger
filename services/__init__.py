import os
import glob
import arrow

modules = glob.glob(os.path.dirname(__file__) + '/*.py')
__all__ = [os.path.basename(f)[:-3] for f in modules]


class Service(object):

    def __init__(self, iftttdir, last_sync):
        self.iftttdir = iftttdir
        self.last_sync = last_sync

    def process_file(self, filename):
        filename = '%s/%s' % (self.iftttdir, filename)
        return open(filename).read().split('@done')[:-1]

    def get_entries(self, service, parts):
        entries = []
        for n in parts:
            p = n.lstrip().split('|~|')
            day = arrow.get(p[0], 'MMMM DD, YYYY at HH:mmA')

            if day.datetime > arrow.get(self.last_sync):
                entries.append({
                    'service': service,
                    'date': day,
                    'values': p[1:]
                    })
        return entries

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

