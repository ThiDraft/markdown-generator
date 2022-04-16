from .helper import MarkdownTestCase
from markdown_generator import link


class LinkTest(MarkdownTestCase):
    def test_empty_link(self):
        self.assertEqual(link(''), '')

    def test_none_link(self):
        self.assertEqual(link(None), '')

    def test_valid_link(self):
        url = 'example.com'
        self.assertEqual(link(url), url)

    def test_valid_link_none_text(self):
        url = 'example.com'
        self.assertEqual(link(url, None), url)

    def test_valid_link_empty_text(self):
        url = 'example.com'
        self.assertEqual(link(url, ''), url)

    def test_valid_link_with_text(self):
        url = 'example.com'
        text = 'see example'
        self.assertEqual(link(url, text), f'[{text}]({url})')
