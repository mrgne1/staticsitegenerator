
from textnode import TextNode 
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    return [n  for o in old_nodes for n in split_node(o, delimiter, text_type)]


def split_node(node, delimiter, text_type):
    if node.text_type != "text":
        return [node]

    segments = node.text.split(delimiter)

    if len(segments) == 1:
        return [node]

    if len(segments) % 2 != 1:
        raise Exception(f"Invalid markdown: unmatched '{delimiter}'")
    
    nodes = []
    for i, s in enumerate(segments):
        if i % 2 == 1:
            nodes.append(TextNode(s, text_type))
        elif s:
            nodes.append(TextNode(s, node.text_type))
    return nodes

def split_nodes_image(old_nodes):
    image = r"!\[(.*?)\]\((.*?)\)"
    return [n  for o in old_nodes for n in split_node_2_capture_re(node=o, regex=image, text_type="image")]
        
def split_nodes_link(old_nodes):
    link = r"(?<!!)\[(.*?)\]\((.*?)\)"
    return [n  for o in old_nodes for n in split_node_2_capture_re(node=o, regex=link, text_type="link")]

def split_node_2_capture_re(node, regex, text_type):
    if node.text_type != "text":
        return [node]
    
    segments = re.split(regex, node.text)
    segments = list(filter(lambda x: x, segments))
    if len(segments) == 1:
        return [node]

    nodes = []
    isText = len(segments) != 2
    while segments:
        text, segments = segments[0], segments[1:]
        if text and isText:
            nodes.append(TextNode(text=text, text_type="text"))
            isText = False
        elif text:
            url, segments = segments[0], segments[1:]
            nodes.append(TextNode(text=text, text_type=text_type, url=url))
            isText = True

    return nodes

def extract_markdown_images(text):
    image = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(image, text)

def extract_markdown_links(text):
    link = r"(?<!!)\[(.*?)\]\((.*?)\)"
    return re.findall(link, text)
