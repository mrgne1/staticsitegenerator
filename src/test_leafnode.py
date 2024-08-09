import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html_basic(self):
        node = LeafNode("p", "This is a paragraph of text.")
        expected = "<p>This is a paragraph of text.</p>"

        self.assertEqual(expected, node.to_html())

    def test_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected = '<a href="https://www.google.com">Click me!</a>'

        self.assertEqual(expected, node.to_html())

    @unittest.expectedFailure
    def test_none_value(self):
        node = LeafNode("a", None, {"href": "https://www.google.com"})

    @unittest.expectedFailure
    def test_none_value_to_html(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node.value = None
        html = node.to_html()
    

if __name__ == "__main__":
    unittest.main()
