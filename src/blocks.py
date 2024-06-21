from htmlnode import *
from textnode import *
import re
from utility import *


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    new_blocks = []
    if markdown:
        for block in raw_blocks:
            if block != '\n' or block != "":
                block = block.strip()
                new_blocks.append(block)
    return new_blocks


def block_to_block_type(block):
    if block[0] == '#' and block[:7] != '#######':
        return BlockType.HEADING
    elif block[:3] == '```' and block[-3:] == '```':
        return BlockType.CODE
    elif block[0] == '>':
        quote = True
        for line in block.split('\n'):
            if line[0] != '>':
                quote = False
                break
        if quote:
            return BlockType.QUOTE
    elif block[:2] == '* ' or block[:2] == '- ':
        unordered = True
        for line in block.split('\n'):
            if line[:2] != '* ' and line[:2] != '- ':
                unordered = False
                break
        if unordered:
            return BlockType.UNORDERED_LIST
    elif block[:3] == '1. ':
        ordered = True
        i = 1
        for line in block.split('\n'):
            if line[:3] != f'{i}. ':
                ordered = False
                break
            i += 1
        if ordered:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_text_nodes(text)
    children = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children


def quote_block_to_htmlnode(block):
    new_block = []
    for line in block.split('\n'):
        line = line.lstrip('>').lstrip()
        if line:
            new_block.append(line)
    result = "\n".join(new_block)
    children = text_to_children(result)
    return ParentNode("blockquote", children)


def heading_block_to_htmlnode(block):
    heading_number = 0
    for letter in block[:6]:
        if letter == '#':
            heading_number += 1
        else:
            break
    children = text_to_children(block.lstrip('#').lstrip())
    return ParentNode(f"h{heading_number}", children)


def code_block_to_htmlnode(block):
    processed_block = block[4:-3]
    children = text_to_children(processed_block)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def unordered_list_block_to_htmlnode(block):
    children = []
    for line in block.split("\n"):
        text = line[2:]
        inline_children = text_to_children(text)
        children.append(ParentNode("li", inline_children))
    return ParentNode("ul", children)


def ordered_list_block_to_htmlnode(block):
    children = []
    for line in block.split("\n"):
        text = line[3:]
        inline_children = text_to_children(text)
        children.append(ParentNode("li", inline_children))
    return ParentNode("ol", children)


def paragraph_block_to_htmlnode(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.QUOTE:
                nodes.append(quote_block_to_htmlnode(block))
            case BlockType.HEADING:
                nodes.append(heading_block_to_htmlnode(block))
            case BlockType.CODE:
                nodes.append(code_block_to_htmlnode(block))
            case BlockType.UNORDERED_LIST:
                nodes.append(unordered_list_block_to_htmlnode(block))
            case BlockType.ORDERED_LIST:
                nodes.append(ordered_list_block_to_htmlnode(block))
            case BlockType.PARAGRAPH:
                nodes.append(paragraph_block_to_htmlnode(block))
    return ParentNode("div", nodes)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = open(from_path).read()
    template = open(template_path).read()
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    dest_path_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_path_dir):
        os.mkdir(dest_path_dir)
    open(dest_path, 'w').write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for element in os.listdir(dir_path_content):
        path = os.path.join(dir_path_content, element)
        dest_dir = os.path.join(dest_dir_path, element)
        print(f"current element: {path}\n"
              f"It's a file: {os.path.isfile(path)}\n"
              f"{path[-3:]} ends on '.md': {path[-3:] == '.md'}\n"
              f"It's a directory: {os.path.isdir(path)}")
        print(f"dest_dir_path: {dest_dir_path}, path: {path}, dest_dir: {dest_dir}")
        if os.path.isfile(path):
            if path[-3:] == '.md':
                dest_dir = os.path.join(dest_dir_path, element).replace('.md', '.html')
                generate_page(path, template_path, dest_dir)
        else:
            dest_dir = os.path.join(dest_dir_path, element)
            if os.path.isdir(path):
                generate_pages_recursive(path, template_path, dest_dir)
