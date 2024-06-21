import os
import shutil

from htmlnode import *
from textnode import *
from enum import Enum
import re

VALID_DELIMITERS = {'`', '*', '**'}


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


def text_to_text_nodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(text_node.text)
        case TextType.BOLD:
            return LeafNode(text_node.text, "b")
        case TextType.ITALIC:
            return LeafNode(text_node.text, "i")
        case TextType.CODE:
            return LeafNode(text_node.text, "code")
        case TextType.LINK:
            return LeafNode(text_node.text, "a", {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("", "img", {"src": text_node.url, "alt": text_node.text})


def split_nodes_delimiter(old_nodes, delimiter, text_type: TextType):
    if delimiter not in VALID_DELIMITERS:
        raise ValueError(f"Invalid delimiter {delimiter}")
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT and isinstance(node, TextNode):
            new_nodes.append(node)
        else:
            split_nodes = node.text.split(delimiter)
            if len(split_nodes) % 2 == 0:
                raise ValueError(f"No closing {text_type} delimiter")
            for i, part in enumerate(split_nodes):
                if part != "":
                    if i % 2 == 0:
                        new_nodes.append(TextNode(part, TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(part, text_type))
                else:
                    if i % 2 != 0:
                        new_nodes.append(TextNode(part, text_type))
    return new_nodes


def extract_markdown_images(text):
    content = []
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    for match in matches:
        content.append(match)
    return content


def extract_markdown_links(text):
    content = []
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    for match in matches:
        content.append(match)
    return content


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        image_tuples = extract_markdown_images(text)
        if not image_tuples:
            if text != "":
                new_nodes.append(node)
        else:
            for image_tup in image_tuples:
                split_node = text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
                if split_node[0] != "":
                    new_nodes.append(TextNode(split_node[0], TextType.TEXT))
                new_nodes.append(TextNode(image_tup[0], TextType.IMAGE, image_tup[1]))
                text = split_node[1]
            if text != '':
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        link_tuples = extract_markdown_links(text)
        if not link_tuples:
            if text != "":
                new_nodes.append(node)
        else:
            for link_tup in link_tuples:
                split_node = text.split(f"[{link_tup[0]}]({link_tup[1]})", 1)
                if split_node[0] != "":
                    new_nodes.append(TextNode(split_node[0], TextType.TEXT))
                new_nodes.append(TextNode(link_tup[0], TextType.LINK, link_tup[1]))
                text = split_node[1]
            if text != '':
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def copy_dir_to_new_dir(old, new):
    if not os.path.exists(old):
        print("path doesn't exist")
        return None
    if os.path.exists(new):
        shutil.rmtree(new)
    os.mkdir(new)
    entries = os.listdir(old)
    for entry in entries:
        path = os.path.join(old, entry)
        if os.path.isfile(path):
            shutil.copy(path, new)
        else:
            new_path = os.path.join(new, entry)
            os.mkdir(new_path)
            copy_dir_to_new_dir(path, new_path)


def extract_title(markdown):
    if not markdown.startswith('#'):
        raise Exception("No h1 header in markdown")
    return markdown.split('#')[1].split('#')[0]  #returns string between two hashtags
