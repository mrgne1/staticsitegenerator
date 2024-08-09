
import unittest
import stringer
from textnode import TextNode

class TestStringerSplitNodesDelimiter(unittest.TestCase):

    def test_not_text(self):
        old_nodes = [TextNode(text="content", text_type="bold")]
        new_nodes = stringer.split_nodes_delimiter(old_nodes, "**", "italic")

        self.assertEqual(old_nodes, new_nodes)

    def test_only_bold(self):
        old_nodes = [TextNode(text="*content*", text_type="text")]
        new_nodes = stringer.split_nodes_delimiter(old_nodes, "*", "bold")
        expected = [TextNode(text="content", text_type="bold")]

        self.assertEqual(expected, new_nodes)

    def test_text_before(self):
        old_nodes = [TextNode(text="plain *content*", text_type="text")]
        new_nodes = stringer.split_nodes_delimiter(old_nodes, "*", "bold")
        expected = [
            TextNode(text="plain ", text_type="text"),
            TextNode(text="content", text_type="bold"),
        ]

        self.assertEqual(expected, new_nodes)

    def test_text_after(self):
        old_nodes = [TextNode(text="*content* plain", text_type="text")]
        new_nodes = stringer.split_nodes_delimiter(old_nodes, "*", "bold")
        expected = [
            TextNode(text="content", text_type="bold"),
            TextNode(text=" plain", text_type="text"),
        ]

        self.assertEqual(expected, new_nodes)

    def test_no_delimiter(self):
        old_nodes = [TextNode(text="content", text_type="text")]
        new_nodes = stringer.split_nodes_delimiter(old_nodes, "**", "italic")

        self.assertEqual(old_nodes, new_nodes)

    @unittest.expectedFailure
    def test_unmatched_delimiter(self):
        old_nodes = [TextNode(text="**content", text_type="text")]
        new_nodes = stringer.split_nodes_delimiter(old_nodes, "**", "italic")


class TestStringerExtractMarkdownImages(unittest.TestCase):
    def test_no_images(self):
        images = stringer.extract_markdown_images("plain text")
        expected = []

        self.assertEqual(expected, images)

    def test_only_image(self):
        images = stringer.extract_markdown_images("![rick roll](https://i.imgur.com/aKaOqIh.gif)")
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]

        self.assertEqual(expected, images)

    def test_one_image(self):
        images = stringer.extract_markdown_images("his is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and")
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]

        self.assertEqual(expected, images)

    def test_two_images(self):
        images = stringer.extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpg)")
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpg")]

        self.assertEqual(expected, images)

    def test_one_image_one_link(self):
        images = stringer.extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpg)")
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]

        self.assertEqual(expected, images)

class TestStringerExtractMarkdownLinks(unittest.TestCase):
    def test_no_links(self):
        links = stringer.extract_markdown_links("plain text")
        expected = []

        self.assertEqual(expected, links)

    def test_only_link(self):
        links = stringer.extract_markdown_links("[to boot dev](https://www.boot.dev)")
        expected = [("to boot dev", "https://www.boot.dev")]

        self.assertEqual(expected, links)

    def test_one_link(self):
        links = stringer.extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and ")
        expected = [("to boot dev", "https://www.boot.dev")]

        self.assertEqual(expected, links)

    def test_two_links(self):
        links = stringer.extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

        self.assertEqual(expected, links)

    def test_one_link_one_image(self):
        links = stringer.extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)")
        expected = [("to boot dev", "https://www.boot.dev")]

        self.assertEqual(expected, links)

class TestStringerSplitNodesImage(unittest.TestCase):

    def test_no_image(self):
        old_nodes = [TextNode("text", "text")]
        new_nodes = stringer.split_nodes_image(old_nodes)

        self.assertEqual(old_nodes, new_nodes)

    def test_only_image(self):
        old_nodes = [
            TextNode(
                "![to boot dev](https://www.boot.dev/img.gif)",
                "text",
            )
        ]
        expected = [
            TextNode(text="to boot dev", text_type="image", url="https://www.boot.dev/img.gif"),
        ]
        
        new_nodes = stringer.split_nodes_image(old_nodes)

        self.assertEqual(expected, new_nodes)

    def test_one_image(self):
        old_nodes = [
            TextNode(
                "This is text with a link ![to boot dev](https://www.boot.dev/img.gif) and",
                "text",
            )
        ]
        expected = [
            TextNode(text="This is text with a link ", text_type="text"),
            TextNode(text="to boot dev", text_type="image", url="https://www.boot.dev/img.gif"),
            TextNode(text=" and", text_type="text"),
        ]
        
        new_nodes = stringer.split_nodes_image(old_nodes)

        self.assertEqual(expected, new_nodes)

    def test_two_images(self):
        old_nodes = [
            TextNode(
                "This is text with a link ![to boot dev](https://www.boot.dev/img.gif) and ![to youtube](https://www.youtube.com/@bootdotdev/img.jpeg)",
                "text",
            )
        ]
        expected = [
            TextNode(text="This is text with a link ", text_type="text"),
            TextNode(text="to boot dev", text_type="image", url="https://www.boot.dev/img.gif"),
            TextNode(text=" and ", text_type="text"),
            TextNode(text="to youtube", text_type="image", url="https://www.youtube.com/@bootdotdev/img.jpeg"),
        ]
        
        new_nodes = stringer.split_nodes_image(old_nodes)

        self.assertEqual(expected, new_nodes)

    def test_one_image_one_link(self):
        old_nodes = [
            TextNode(
                "This is text with a link ![to boot dev](https://www.boot.dev/img.gif) and [to youtube](https://www.youtube.com/@bootdotdev)",
                "text",
            )
        ]
        expected = [
            TextNode(text="This is text with a link ", text_type="text"),
            TextNode(text="to boot dev", text_type="image", url="https://www.boot.dev/img.gif"),
            TextNode(text=" and [to youtube](https://www.youtube.com/@bootdotdev)", text_type="text"),
        ]
        
        new_nodes = stringer.split_nodes_image(old_nodes)

        self.assertEqual(expected, new_nodes)

class TestStringerSplitNodesLink(unittest.TestCase):

    def test_no_link(self):
        old_nodes = [TextNode("text", "text")]
        new_nodes = stringer.split_nodes_link(old_nodes)

        self.assertEqual(old_nodes, new_nodes)

    def test_only_link(self):
        old_nodes = [
            TextNode(
                "[to boot dev](https://www.boot.dev/img.gif)",
                "text",
            )
        ]
        expected = [
            TextNode(text="to boot dev", text_type="link", url="https://www.boot.dev/img.gif"),
        ]
        
        new_nodes = stringer.split_nodes_link(old_nodes)

        self.assertEqual(expected, new_nodes)

if __name__ == "__main__":
    unittest.main()