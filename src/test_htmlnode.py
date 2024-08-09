import unittest

from htmlnode import HtmlNode

class TestHtmlNode(unittest.TestCase):
    def test_empty_repr(self):
        node = HtmlNode()
        node2 = HtmlNode()

        self.assertEqual(str(node), str(node2))

    def test_tag_repr(self):
        node = HtmlNode("h1")
        node2 = HtmlNode("h1")

        self.assertEqual(str(node), str(node2))

    def test_value_repr(self):
        node = HtmlNode(value="value")
        node2 = HtmlNode(value="value")

        self.assertEqual(str(node), str(node2))

    def test_children_repr(self):
        node = HtmlNode(children=[])
        node2 = HtmlNode(children=[])

        self.assertEqual(str(node), str(node2))

    def test_props_repr(self):
        node = HtmlNode(props={"height": 10})
        node2 = HtmlNode(props={"height": 10})

        self.assertEqual(str(node), str(node2))

    def test_props_to_html(self):
        node = HtmlNode(props={"href": "https://www.google.com", "target": "_blank"})
        html_props = node.props_to_html()
        self.assertIn(' href="https://www.google.com"', html_props)
        self.assertIn(' target="_blank"', html_props)

    def test_empty_props_to_html(self):
        node = HtmlNode()
        html_props = node.props_to_html()
        self.assertEqual("", html_props)



if __name__ == "__main__":
    unittest.main()