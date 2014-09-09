from . import Service


class tracks(Service):

    service = 'tracks'

    def parse(self):
        parts = self.process_file('tracks.txt')
        entries = self.get_entries(self.service, parts)

        for e in entries:
            e['md'] = '- %s: *%s* by **%s**' % (
                e['date'].format('HH:mm'),
                e['values'][0].strip(),
                e['values'][1].strip(),
            )
        return entries
