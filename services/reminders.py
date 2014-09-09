from . import Service


class reminders(Service):

    service = 'reminders'

    def parse(self):
        parts = self.process_file('reminders.txt')
        entries = self.get_entries(self.service, parts)

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
