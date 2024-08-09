import unittest
from textnode import TextNode
import converter

class TestConverterTextNodeToHtmlNode(unittest.TestCase):

    def test_convert_text(self):
        node = TextNode("content", "text")
        cnode = converter.text_node_to_html_node(node)

        expected = "content"
        self.assertEqual(expected, cnode.to_html())

    def test_convert_bold(self):
        node = TextNode("content", "bold")
        cnode = converter.text_node_to_html_node(node)

        expected = "<b>content</b>"
        self.assertEqual(expected, cnode.to_html())

    def test_convert_italic(self):
        node = TextNode("content", "italic")
        cnode = converter.text_node_to_html_node(node)

        expected = "<i>content</i>"
        self.assertEqual(expected, cnode.to_html())
        self.assertEqual(expected, cnode.to_html())

    def test_convert_code(self):
        node = TextNode("content", "code")
        cnode = converter.text_node_to_html_node(node)

        expected = "<code>content</code>"
        self.assertEqual(expected, cnode.to_html())

    def test_convert_link(self):
        node = TextNode("content", "link", "www.google.com")
        cnode = converter.text_node_to_html_node(node)

        expected = '<a href="www.google.com">content</a>'
        self.assertEqual(expected, cnode.to_html())

    def test_convert_image(self):
        node = TextNode("alt text", "image", "www.google.com")
        cnode = converter.text_node_to_html_node(node)

        expected = '<img src="www.google.com" alt="alt text"></img>'
        self.assertEqual(expected, cnode.to_html())

class TestConverterTextToTextNodes(unittest.TestCase):

    def test_full(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode("obi wan image", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
        ]
        nodes = converter.text_to_textnodes(text)

        self.assertEqual(expected, nodes)


class TestConverterMarkdownToBlocks(unittest.TestCase):

    def test_single_block(self):
        markdown = "# This is a heading"
        expected = [markdown]
        blocks = converter.markdown_to_blocks(markdown)

        self.assertEqual(expected, blocks)

    def test_two_blocks(self):
        b1 = "# This is a heading"
        b2 = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        markdown = f"{b1}\n\n{b2}"
        expected = [b1, b2]

        blocks = converter.markdown_to_blocks(markdown)

        self.assertEqual(expected, blocks)

    def test_multiline_block(self):
        b1 = "# This is a heading"
        b2 = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        markdown = f"{b1}\n{b2}"
        expected = [markdown]

        blocks = converter.markdown_to_blocks(markdown)

        self.assertEqual(expected, blocks)

    def test_boot_dev_example(self):
        b1 = "# This is a heading"
        b2 = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        l1 = "* This is the first list item in a list block"
        l2 = "* This is a list item"
        l3 = "* This is another list item"
        b3 = f"{l1}\n{l2}\n{l3}"
        markdown = f"{b1}\n\n{b2}\n\n{b3}"

        expected = [b1, b2, b3]

        blocks = converter.markdown_to_blocks(markdown)

        self.assertEqual(expected, blocks)

    def test_strip_whitespace(self):
        b1 = "# This is a heading"
        b2 = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        l1 = "* This is the first list item in a list block"
        l2 = "* This is a list item"
        l3 = "* This is another list item"
        b3 = f"{l1}\n{l2}\n{l3}"
        markdown = f" {b1} \n\n {b2} \n\n {b3} "

        expected = [b1, b2, b3]

        blocks = converter.markdown_to_blocks(markdown)

        self.assertEqual(expected, blocks)

class TestConverterBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        block = "# h1"
        expected = "heading"
        block_type = converter.block_to_block_type(block)

        self.assertEqual(expected, block_type)

    def test_heading2(self):
        block = "## h1"
        expected = "heading"
        block_type = converter.block_to_block_type(block)

        self.assertEqual(expected, block_type)

    def test_heading3(self):
        block = "### h1"
        expected = "heading"
        block_type = converter.block_to_block_type(block)

        self.assertEqual(expected, block_type)

    def test_heading4(self):
        block = "#### h1"
        expected = "heading"
        block_type = converter.block_to_block_type(block)

        self.assertEqual(expected, block_type)

    def test_heading5(self):
        block = "##### h1"
        expected = "heading"
        block_type = converter.block_to_block_type(block)

        self.assertEqual(expected, block_type)

    def test_heading6(self):
        block = "###### h1"
        expected = "heading"
        block_type = converter.block_to_block_type(block)

        self.assertEqual(expected, block_type)

    def test_heading7(self):
        block = "####### h1"
        expected = "paragraph"
        block_type = converter.block_to_block_type(block)

        self.assertEqual(expected, block_type)

    def test_code(self):
        block = "```code```"
        expected = "code"
        block_type = converter.block_to_block_type(block)

        self.assertEqual(expected, block_type)

    def test_code_unmatched1(self):
        block = "```code"
        expected = "paragraph"
        block_type = converter.block_to_block_type(block)

        self.assertEqual(expected, block_type)

    def test_code_unmatched2(self):
        block = "code```"
        expected = "paragraph"
        block_type = converter.block_to_block_type(block)

        self.assertEqual(expected, block_type)

    def test_singleline_quote(self):
        block = ">quote"
        expected = "quote"
        block_type = converter.block_to_block_type(block)

        self.assertEqual(expected, block_type)

    def test_multiline_quote(self):
        block = ">quote\n>line2"
        expected = "quote"
        block_type = converter.block_to_block_type(block)

        self.assertEqual(expected, block_type)

    def test_non_quote(self):
        block = ">quote\nline2"
        expected = "paragraph"
        block_type = converter.block_to_block_type(block)

        self.assertEqual(expected, block_type)

    def test_singleline_unordered_list(self):
        block = "* unordered_list"
        expected = "unordered_list"
        block_type = converter.block_to_block_type(block)

        self.assertEqual(expected, block_type)

    def test_multiline_unordered_list(self):
        block = "* unordered_list\n* line2"
        expected = "unordered_list"
        block_type = converter.block_to_block_type(block)

        self.assertEqual(expected, block_type)

    def test_non_unordered_list(self):
        block = "* unordered_list\nline2"
        expected = "paragraph"
        block_type = converter.block_to_block_type(block)

        self.assertEqual(expected, block_type)

    def test_singleline_unordered_list_dash(self):
        block = "- unordered_list"
        expected = "unordered_list"
        block_type = converter.block_to_block_type(block)

        self.assertEqual(expected, block_type)

    def test_multiline_unordered_list_dash(self):
        block = "- unordered_list\n- line2"
        expected = "unordered_list"
        block_type = converter.block_to_block_type(block)

        self.assertEqual(expected, block_type)

    def test_non_unordered_list_dash(self):
        block = "- unordered_list\nline2"
        expected = "paragraph"
        block_type = converter.block_to_block_type(block)

        self.assertEqual(expected, block_type)

    def test_singleline_ordered_list(self):
        block = "1. ordered_list"
        expected = "ordered_list"
        block_type = converter.block_to_block_type(block)

        self.assertEqual(expected, block_type)

    def test_multiline_ordered_list(self):
        block = "1. ordered_list\n2. line2"
        expected = "ordered_list"
        block_type = converter.block_to_block_type(block)

        self.assertEqual(expected, block_type)

    def test_non_ordered_list(self):
        block = "1. ordered_list\nline2"
        expected = "paragraph"
        block_type = converter.block_to_block_type(block)

        self.assertEqual(expected, block_type)


    def test_paragraph(self):
        block = "#paragraph\nhere"
        expected = "paragraph"
        block_type = converter.block_to_block_type(block)

        self.assertEqual(expected, block_type)

class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_simple_paragraph(self):
        node = converter.markdown_to_html_node("some text")
        expected = "<div><p>some text</p></div>"

        html = node.to_html()
        self.assertEqual(expected, html)

    def test_simple_code(self):
        node = converter.markdown_to_html_node("```code```")
        expected = "<div><pre><code>code</code></pre></div>"

        html = node.to_html()
        self.assertEqual(expected, html)
    
    def test_simple_quote(self):
        node = converter.markdown_to_html_node("> quote\n>second quote")
        expected = "<div><blockquote>quote second quote</blockquote></div>"

        html = node.to_html()
        self.assertEqual(expected, html)

    def test_example_quote(self):
        node = converter.markdown_to_html_node("> All that is gold does not glitter")
        expected = "<div><blockquote>All that is gold does not glitter</blockquote></div>"

        html = node.to_html()
        self.assertEqual(expected, html)


    def test_simple_header(self):
        node = converter.markdown_to_html_node("## header")
        expected = "<div><h2>header</h2></div>"

        html = node.to_html()
        self.assertEqual(expected, html)

    def test_simple_ul(self):
        node = converter.markdown_to_html_node("* element 1\n* element b")
        expected = "<div><ul><li>element 1</li><li>element b</li></ul></div>"

        html = node.to_html()
        self.assertEqual(expected, html)

    def test_simple_ul_dash(self):
        node = converter.markdown_to_html_node("- element 1\n- element b")
        expected = "<div><ul><li>element 1</li><li>element b</li></ul></div>"

        html = node.to_html()
        self.assertEqual(expected, html)


    def test_simple_ol(self):
        node = converter.markdown_to_html_node("1. element 1\n2. element b")
        expected = "<div><ol><li>element 1</li><li>element b</li></ol></div>"

        html = node.to_html()
        self.assertEqual(expected, html)

    def test_all_simple(self):
        blocks = [
            "some text",
            "```code```",
            "> quote\n>second quote",
            "## header",
            "* element 1\n* element b",
            "1. element 1\n2. element b",
        ] 
        markdown = "\n\n".join(blocks)
        node = converter.markdown_to_html_node(markdown)
        expected = "<div><p>some text</p><pre><code>code</code></pre><blockquote>quote second quote</blockquote><h2>header</h2><ul><li>element 1</li><li>element b</li></ul><ol><li>element 1</li><li>element b</li></ol></div>"
        
        html = node.to_html()
        self.assertEqual(expected, html)

if __name__ == "__main__":
    unittest.main()