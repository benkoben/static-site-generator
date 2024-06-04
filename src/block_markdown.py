import re

from enum import Enum
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextTypes

HEADER_REGEX = r"(?<!#)(#{1,6})\s(.*)?"

class BlockTypes(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST =  "ordered list"

def markdown_to_blocks(text):
    blocks = list()
    for block in text.lstrip("\n").rstrip("\n").split("\n\n"):
        blocks.append(block)
    return blocks

def block_to_block_type(block):
    lines = block.split("\n")

    # Check to see if the block is a header type
    if re.search(HEADER_REGEX, lines[0]):
        return BlockTypes.HEADING
    
    # Header blocks
    if lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockTypes.CODE
    # Code blocks
    if len([x for x in lines if x.startswith(">")]) == len(lines):
        return BlockTypes.QUOTE
    # Unordered list blocks
    if len([x for x in lines if x.startswith("*")]) == len(lines):
        return BlockTypes.UNORDERED_LIST
    # Ordered list blocks
    if lines[0].startswith("1."):
        line_number_index = [True] * len(lines)
        for index, line in enumerate(lines):
            if not line.startswith(f"{index + 1}."):
                del line_number_index[index]
        if len(line_number_index) == len(lines):
            return BlockTypes.ORDERED_LIST
    # Default to paragraph
    return BlockTypes.PARAGRAPH

def header_block_to_html(header_block):
    try:
        header, text = re.findall(HEADER_REGEX, header_block)[0]
    except IndexError:
        raise ValueError("header_block does not contain a valid markdown header")
    
    return LeafNode(f"h{header.count("#")}", text)

def code_block_to_html(code_block):
    lines = code_block.split("\n")
    if not lines[0].startswith("```") or not lines[-1].startswith("```"):
        raise ValueError("code_block is missing opening/closing characters \"```\"")
    
    children = list()
    for line in lines[1:-1]:
        children.append(TextNode(line, TextTypes.TEXT))

    return ParentNode("pre", ParentNode("code", children))

def quote_block_to_html(quote_block):    
    children = list()
    for line in quote_block.split("\n"):
        children.append(TextNode(line, TextTypes.TEXT))

    return ParentNode("pre", ParentNode("code", children))


def unordered_list_block_to_html(unordered_list_block):
    pass

def ordered_list_block_to_html(ordered_list_block):
    pass

def markdown_to_html(markdown):
    pass

# Debugging 
if __name__ == "__main__":
    code_test_1 = "```python\nprint('hello world')\n```"
    expected_code_test_1_output = ParentNode("pre", ParentNode("code", [
        TextNode("print('hello world')", TextTypes.TEXT)
    ]))
    print(code_block_to_html(code_test_1))
    print(expected_code_test_1_output)