from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode
import stringer
import re

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case "text":
            return LeafNode(value=text_node.text)
        case "bold":
            return LeafNode(tag="b", value=text_node.text)
        case "italic":
            return LeafNode(tag="i", value=text_node.text)
        case "code":
            return LeafNode(tag="code", value=text_node.text)
        case "link":
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case "image":
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unknown text type '{text_node.text_type}'")

def text_to_textnodes(text):
    nodes = [TextNode(text=text, text_type="text")]
    nodes = stringer.split_nodes_delimiter(nodes, "**", "bold")
    nodes = stringer.split_nodes_delimiter(nodes, "*", "italic")
    nodes = stringer.split_nodes_delimiter(nodes, "`", "code")
    nodes = stringer.split_nodes_image(nodes)
    nodes = stringer.split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [b.strip() for b in blocks]
    blocks = [b for b in blocks if b]
    return blocks

def block_to_block_type(block):
    headingre = r"^#{1,6} "
    if re.match(headingre, block):
        return "heading"
    elif block.startswith("```") and block.endswith("```"):
        return "code"
    elif all_lines_startwith(block, ">"):
        return "quote"
    elif all_lines_startwith(block, "* "):
        return "unordered_list"
    elif all_lines_startwith(block, "- "):
        return "unordered_list"
    elif is_ordered_list(block):
        return "ordered_list"
    else:
        return "paragraph"

def all_lines_startwith(block, start):
    return all([b.startswith(start) for b in block.split("\n")])

def is_ordered_list(block):
    lines = block.split("\n")
    indexre = r"^(\d+). "

    for i, l in enumerate(lines, 1):
        try:
            not_right_index = i != int(re.findall(indexre, l)[0])
        except:
            return False
        else:
            if not_right_index:
                return False

    return True

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    headerre = r"(#{1,6}) (.*)"
    olre = r"\d+. (.*)"
    ulre = r"[*-] (.*)"

    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "heading":
            marker, text = re.findall(headerre, block)[0]
            children.append(ParentNode(tag=f"h{len(marker)}", children=text_to_html_nodes(text)))
        elif block_type == "code":
            pre_children = [LeafNode(tag="code", value=block.replace("```", ""))]
            children.append(ParentNode(tag="pre", children=pre_children))
        elif block_type == "quote":
            quote = block[1:].replace("\n>", " ").strip()
            children.append(ParentNode(tag="blockquote", children=text_to_html_nodes(quote)))
        elif block_type == "unordered_list":
            lines = [re.findall(ulre, line)[0] for line in block.split("\n")]
            ul_children = [ParentNode(tag="li", children=text_to_html_nodes(line)) for line in lines]
            children.append(ParentNode(tag="ul", children=ul_children))
        elif block_type == "ordered_list":
            lines = [re.findall(olre, line)[0] for line in block.split("\n")]
            ul_children = [ParentNode(tag="li", children=text_to_html_nodes(line)) for line in lines]
            children.append(ParentNode(tag="ol", children=ul_children))
        elif block_type == "paragraph":
            p_children = text_to_html_nodes(block)
            children.append(ParentNode(tag="p", children=p_children))

    html = ParentNode(tag="div", children=children)
    return html


def text_to_html_nodes(text):
    return [text_node_to_html_node(n) for n in text_to_textnodes(text)]

