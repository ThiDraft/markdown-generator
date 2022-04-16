class Code(object):
    def __init__(self, language=None):
        self.language = language
        self.lines = []

    def append(self, text):
        self.lines.append(text)

    def __str__(self):
        if not self.lines:
            return ''
        lang = '' if self.language is None else self.language
        lines = [f'```{lang}']
        lines.extend(self.lines)
        lines.append('```')
        return '\n'.join(lines) + '\n'
