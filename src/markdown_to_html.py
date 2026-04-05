from block_markdown import *
from block import *
from inline_markdown import *
from textnode import *
from htmlnode import *
import re


def markdown_to_html(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    children = []
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            # Convert markdown to HTML for paragraph
            children.append(paragraph_to_html_node(block))
        elif block_type == BlockType.HEADING:
            # Convert markdown to HTML for heading
            children.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            # Convert markdown to HTML for code block
            children.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            # Convert markdown to HTML for quote block
            children.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            # Convert markdown to HTML for unordered list
            children.append(unordered_list_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            # Convert markdown to HTML for ordered list
            children.append(ordered_list_to_html_node(block))
    return ParentNode("div", children)


def text_to_children(text):
    inline_markdown = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        inline_markdown.append(text_node_to_html_node(node))
    return inline_markdown


def paragraph_to_html_node(block):
    text = " ".join(block.splitlines())
    return ParentNode("p", text_to_children(text))


def heading_to_html_node(block):
    block_split = block.split(" ", 1)
    heading_level = len(block_split[0])
    text = block_split[1]
    return ParentNode(f"h{heading_level}", text_to_children(text))


def code_to_html_node(block):
    clean_block = block[4:-3]  # Remove the ``` from the start and end
    return ParentNode("pre",[ParentNode("code", [text_node_to_html_node(TextNode(clean_block, TextType.TEXT))])])


def quote_to_html_node(block):
    text_lines = block.splitlines()
    clean_lines = []
    for line in text_lines:
        clean_lines.append(line[1:].strip())  # Remove the > from the start of each line
    text = " ".join(clean_lines)
    return ParentNode("blockquote", text_to_children(text))


def unordered_list_to_html_node(block):
    text_lines = block.splitlines()
    clean_lines = []
    for line in text_lines:
        clean_lines.append(line[1:].strip())  # Remove the - from the start of each line
    return ParentNode("ul", [ParentNode("li", text_to_children(line)) for line in clean_lines])


def ordered_list_to_html_node(block):
    text_lines = block.splitlines()
    clean_lines = []
    for line in text_lines:
        clean_text = re.sub(r"^\d+\.\s+", "", line)
        clean_lines.append(clean_text)
    return ParentNode("ol", [ParentNode("li", text_to_children(line)) for line in clean_lines])