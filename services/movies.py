from . import Service

# optional: it's used to remove your IMDb username from the
#           feed: 'lardissone rated 7' > 'rated 7'
IMDB_USERNAME = 'lardissone'


class movies(Service):

    service = 'movies'

    def parse(self):
        parts = self.process_file('movies.txt')
        entries = self.get_entries(self.service, parts)

        for e in entries:
            e['md'] = '- %s: **%s**: %s' % (
                e['date'].format('HH:mm'),
                e['values'][0].strip(),
                e['values'][1].replace(IMDB_USERNAME, '').strip(),
            )
        return entries
