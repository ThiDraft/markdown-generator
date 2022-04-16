import unittest
from markdown_generator import Writer
from ddt import ddt, data, unpack
from os import linesep


class Data(dict):
    def __init__(self, item=None, **elements):
        dict.__init__(self, item=item, **elements)
        setattr(self, '__name__', type(item).__name__)


class HeadingData(Data):
    def __init__(self, item=None, level=1, **elements):
        Data.__init__(self, level=level, item=item, **elements)
        setattr(self, '__name__', getattr(self, '__name__') + str(level))


class MockFile(object):
    def __init__(self):
        self.content = ''

    def clear(self):
        self.content = ''

    def write(self, text):
        self.content += text

    def read(self):
        content = self.content
        self.clear()
        return content


WRITE_TEST_DATA = [Data(item) for item in [
    'text',
]]
HEADER_TEST_DATA = [
    HeadingData(level=n, **d)
    for n in range(1, 7)
    for d in WRITE_TEST_DATA
]


@ddt
class WriterTest(unittest.TestCase):
    def setUp(self):
        self.stdout = MockFile()
        self.writer = Writer(self.stdout)

    def assertReadEqual(self, text, msg=None):
        self.assertEqual(self.stdout.read(), text, msg=msg)

    def test_no_writes(self):
        self.assertReadEqual('')

    @data(*WRITE_TEST_DATA)
    @unpack
    def test_write(self, item):
        self.writer.write(item)
        self.assertReadEqual(str(item))

    @data(*WRITE_TEST_DATA)
    @unpack
    def test_writeline(self, item):
        self.writer.writeline(item)
        self.assertReadEqual(str(item) + linesep)

    def test_writelines(self):
        self.writer.writelines(WRITE_TEST_DATA)
        expected = linesep.join(map(str, WRITE_TEST_DATA)) + linesep
        self.assertReadEqual(expected)

    @data(*HEADER_TEST_DATA)
    @unpack
    def test_write_heading(self, item, level):
        self.writer.write_heading(item, level)
        self.assertReadEqual(''.ljust(level, '#') + ' ' + str(item) + linesep)

    def test_write_hrule(self):
        self.writer.write_hrule()
        self.assertReadEqual(f'---{linesep}')
