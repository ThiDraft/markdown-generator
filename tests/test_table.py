from .helper import MarkdownTestCase
from markdown_generator import Table, Alignment
from ddt import ddt, data, unpack
from itertools import combinations, permutations


class Data(dict):
    def __init__(self, name, **elements):
        dict.__init__(self, **elements)
        setattr(self, '__name__', name)


def create_test_data(scols='', rows=0):
    cols = [{
                'L': Alignment.LEFT,
                'R': Alignment.RIGHT,
                'C': Alignment.CENTER
            }[c] for c in scols]
    output = ''
    if cols:
        output += '| '
        output += ' | '.join(f'c{i}' for i, _ in enumerate(cols))
        output += ' |\n'
        for col in cols:
            output += '|'
            output += ':' if Alignment.LEFT & col > 0 else ' '
            output += '---'
            output += ':' if Alignment.RIGHT & col > 0 else ' '
        output += '|\n'
        for r in range(rows):
            for c, _ in enumerate(cols):
                output += f'| {r},{c} '
            output += '|\n'
        output += '\n'
    return Data(
        f'{scols}{rows}' if scols else 'Empty',
        columns=cols,
        rows=rows,
        expected=output,
    )


alignments = {
    ''.join(p)
    for r in range(4)
    for c in combinations('LRC', r)
    for p in permutations(c)
}
TEST_DATA = [
    create_test_data(cols, i)
    for cols in alignments
    for i in range(3)
]


@ddt
class TableTest(MarkdownTestCase):
    @data(*TEST_DATA)
    @unpack
    def test_table_format(self, columns=None, rows=0, expected=''):
        if columns is None:
            columns = []
        table = Table()
        for i, col_align in enumerate(columns):
            table.add_column(f'c{i}', col_align)
        for r in range(rows):
            table.append(*(f'{r},{c}' for c in range(len(columns))))
        self.assertRenderedEqual(table, expected)

    def test_error_append_no_columns(self):
        table = Table()
        with self.assertRaises(ValueError):
            table.append('0,0')

    def test_error_append_not_enough_columns(self):
        table = Table()
        table.add_column('c0')
        with self.assertRaises(ValueError):
            table.append('0,0', '0,1')
