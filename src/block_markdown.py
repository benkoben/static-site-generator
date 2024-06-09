import re

from enum import Enum
from leafnode import LeafNode
from parentnode import ParentNode

__HEADER_REGEX = r"(?<!#)(#{1,6})\s(.*)?"

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
    if re.search(__HEADER_REGEX, lines[0]):
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
        header, text = re.findall(__HEADER_REGEX, header_block)[0]
    except IndexError:
        raise ValueError("header_block does not contain a valid markdown header")
    
    return LeafNode(f"h{header.count('#')}", text)

def code_block_to_html(code_block):
    lines = code_block.split("\n")
    if not lines[0].startswith("```") or not lines[-1].startswith("```"):
        raise ValueError("code_block is missing opening/closing characters \"```\"")
    
    children = list()
    for line in lines[1:-1]:
        children.append(LeafNode(value=line))

    return ParentNode("pre", [ParentNode("code", children)])

def quote_block_to_html(quote_block):    
    children = list()
    for line in quote_block.split("\n"):
        if not line.startswith("> "):
            raise ValueError("quote_block does not contain a valid markdown quotation")
        children.append(LeafNode(value=line.lstrip("> ")))

    return ParentNode("blockquote", children)


def unordered_list_block_to_html(unordered_list_block):
    children = list()
    for line in unordered_list_block.split("\n"):
        if not line.startswith("* "):
            raise ValueError("unordered_list_block does not contain a valid unordered list")
        children.append(LeafNode('li', line.lstrip("* ")))

    return ParentNode("ul", children)

def ordered_list_block_to_html(ordered_list_block):
    children = list()
    for line in ordered_list_block.split("\n"):
        if not line[0].isdigit() and line[1] != ".":
            raise ValueError("ordered_list_block does not contain a valid ordered list")

        children.append(LeafNode('li', line[3:]))

    return ParentNode("ol", children)

# I 
def paragraph_block_to_html(paragraph_block):
    return LeafNode("p", paragraph_block)

def markdown_to_html_node(markdown):
    children = list()
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockTypes.HEADING:
            children.append(header_block_to_html(block))
            
        elif block_type == BlockTypes.CODE:
            children.append(code_block_to_html(block))

        elif block_type == BlockTypes.QUOTE:
            children.append(quote_block_to_html(block))

        elif block_type == BlockTypes.UNORDERED_LIST:
            children.append(unordered_list_block_to_html(block))

        elif block_type == BlockTypes.ORDERED_LIST:
            children.append(ordered_list_block_to_html(block))

        else:
            children.append(paragraph_block_to_html(block))

    return ParentNode("div", children)
    

# Debugging 
if __name__ == "__main__":
    pass