from . import Service

class github(Service):

    service = 'github'

    def parse(self):
        parts = self.process_file('github.txt')
        entries = self.get_entries(self.service, parts)

        for e in entries:
            e['md'] = '- %s: %s' % (
                e['date'].format('HH:mm'),
                e['values'][0].strip()
            )
        return entries
