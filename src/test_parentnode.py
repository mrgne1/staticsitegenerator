import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):

    @unittest.expectedFailure
    def test_children_throws_when_none(self):
        node = ParentNode(tag="p", children=None, props=None)
    
    @unittest.expectedFailure
    def test_to_html_throws_when_tag_is_none(self):
        node = ParentNode(tag=None, children=[], props=None)
        html = node.to_html()

    @unittest.expectedFailure
    def test_to_html_throws_when_no_children(self):
        node = ParentNode(tag="p", children=[], props=None)
        html = node.to_html()

    def test_to_html_simple(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"

        html = node.to_html()

        self.assertEqual(expected, html)

    def test_to_html_nested_parentnodes(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                    ]
                ),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        expected = "<p><p><b>Bold text</b>Normal text</p><i>italic text</i>Normal text</p>"

        html = node.to_html()

        self.assertEqual(expected, html)