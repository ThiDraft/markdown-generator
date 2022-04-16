from .alignment import Alignment


class Table(object):
    def __init__(self):
        self.columns = []
        self.entries = []

    def add_column(self, heading, alignment=Alignment.LEFT):
        if isinstance(alignment, int):
            alignment = Alignment(alignment)
        self.columns.append(Column(heading, alignment))

    def append(self, *fields):
        diff = len(self.columns) - len(fields)
        if diff < 0:
            raise ValueError('Table.append(): too many fields given')
        self.entries.append(list(fields) + [None] * diff)

    def format_row(self, fields):
        return ' | '.join([''] + [str(f) for f in fields] + ['']).strip()

    def __str__(self):
        if not self.columns:
            return ''
        titleRow = '|'
        separatorRow = '|'
        for column in self.columns:
            titleRow += f' {column.heading} |'
            separatorRow += f"{':' if bool(Alignment.LEFT & column.alignment) else ' '}---{':' if bool(Alignment.RIGHT & column.alignment) else ' '}|"

        result = '{}\n{}\n'.format(titleRow, separatorRow) + '\n'.join(
            map(self.format_row, self.entries)
        )

        if self.entries:
            result += '\n'
        return result + '\n'


class Column(object):
    def __init__(self, heading, alignment=Alignment.LEFT):
        self.heading = heading
        self.alignment = alignment
