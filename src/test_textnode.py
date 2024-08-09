import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")

        self.assertEqual(node, node2)

    def test_repr_with_none(self):
        node = TextNode("This is a text node", "bold")

        self.assertEqual(node.__repr__(), 'TextNode("This is a text node", "bold", None)')

    def test_repr_full(self):
        node = TextNode("This is a text node", "bold", "url")

        self.assertEqual(node.__repr__(), 'TextNode("This is a text node", "bold", "url")')

    def test_url_is_none(self):
        node = TextNode("This is a text node", "bold")

        self.assertEqual(node.url, None)

if __name__ == "__main__":
    unittest.main()