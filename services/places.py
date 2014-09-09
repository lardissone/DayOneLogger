from . import Service


class places(Service):

    service = 'places'

    def parse(self):
        parts = self.process_file('places.txt')
        entries = self.get_entries(self.service, parts)

        # TODO: add venue URL
        for e in entries:
            map_img = (' ' * 8) + ('![](%s)' % e['values'][1])
            e['md'] = '- %s: **%s**\n%s' % (
                e['date'].format('HH:mm'),
                e['values'][0].strip(),
                map_img
            )
        return entries
