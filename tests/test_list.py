from .helper import MarkdownTestCase
from markdown_generator import List, CheckList


class OrderedList(List):
    def __init__(self):
        List.__init__(self, True)


class UnorderedListTest(MarkdownTestCase):
    def test_empty_list(self):
        self.assertRenderedEqual(List(), '')

    def test_singleton_list(self):
        lst = List()
        lst.append('item')
        self.assertRenderedEqual(lst, '* item\n\n')

    def test_list_with_multiple_items(self):
        lst = List()
        items = [f'item{i}' for i in range(3)]
        [lst.append(x) for x in items]
        expected = '* ' + '\n* '.join(items) + '\n\n'
        self.assertRenderedEqual(lst, expected)


class OrderedListTest(MarkdownTestCase):
    def test_empty_list(self):
        self.assertRenderedEqual(OrderedList(), '')

    def test_singleton_list(self):
        lst = OrderedList()
        lst.append('item')
        self.assertRenderedEqual(lst, '1. item\n\n')

    def test_list_with_multiple_items(self):
        lst = OrderedList()
        items = [f'item{i}' for i in range(3)]
        [lst.append(x) for x in items]
        items = [f'{i + 1}. {x}' for i, x in enumerate(items)]
        expected = '\n'.join(items) + '\n\n'
        self.assertRenderedEqual(lst, expected)


class CheckListTest(MarkdownTestCase):
    def test_empty_list(self):
        self.assertRenderedEqual(CheckList(), '')

    def test_singleton_list(self):
        lst = CheckList()
        lst.append('item')
        self.assertRenderedEqual(lst, '- [ ] item\n\n')

    def test_singleton_list_checked(self):
        lst = CheckList()
        lst.append('item', True)
        self.assertRenderedEqual(lst, '- [x] item\n\n')

    def test_multiple_items(self):
        lst = CheckList()
        items = [f'item{i}' for i in range(3)]
        [lst.append(x) for x in items]
        expected = ''.join('- [ ] {}\n'.format(x) for x in items) + '\n'
        self.assertRenderedEqual(lst, expected)

    def test_multiple_items_checked(self):
        lst = CheckList()
        items = [f'item{i}' for i in range(3)]
        [lst.append(x, True) for x in items]
        expected = ''.join('- [x] {}\n'.format(x) for x in items) + '\n'
        self.assertRenderedEqual(lst, expected)

    def test_multiple_items_mixed(self):
        lst = CheckList()
        items = [(f'item{i}', i % 2 == 0) for i in range(3)]
        [lst.append(*x) for x in items]
        items = ((x, 'x' if y else ' ') for x, y in items)
        expected = ''.join('- [{}] {}\n'.format(x, y) for y, x in items) + '\n'
        self.assertRenderedEqual(lst, expected)
