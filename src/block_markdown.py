import re

def markdown_to_blocks(markdown):
    block = []
    lines = markdown.split("\n\n")
    for line in lines:
        line_to_add = line.strip()
        if line_to_add != "":
            block.append(line_to_add)
    return block

