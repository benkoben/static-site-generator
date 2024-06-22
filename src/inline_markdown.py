import re

from textnode import TextTypes, TextNode

def extract_markdown_images(text):
    image_regex = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(image_regex, text)

def extract_markdown_links(text):
    links_regex = r"[^!]?\[(.*?)\]\((.*?)\)"
    return re.findall(links_regex, text)

# TODO: Implement a way to split nested nodes by dynamically detecting delimiters
"""
    Split nodes limiter splits all_nodes into chunked new nodes based on the delimiter/text_type.
    It returns a list of nodes.
"""
def split_nodes_delimiter(old_nodes:list, delimiter:str, text_type:TextTypes):
    padding = 1
    if text_type == TextTypes.BOLD:
        padding = 2

    nodes = list()
    for node in old_nodes:
        
        if not node.text_type.name == TextTypes.TEXT.name:
            nodes.append(node)

        elif delimiter in node.text:

            start = node.text.index(delimiter) + padding
            if not delimiter in node.text[start:]:
                raise ValueError(f"Expected closing delimiter \"{delimiter}\" in string \"{node.text}\" but found none")
            stop = start + node.text[start:].index(delimiter)

            # Add text before the delimiter to the nodes
            nodes.append(TextNode(node.text[:start-padding], TextTypes.TEXT))

            # Breakup the current node into multiple nodes and recursively sort them out
            chunks = list()
            chunks.append(TextNode(node.text[start:stop], text_type))

            if len(node.text[stop+padding:]) > 0:
                chunks.append(TextNode(node.text[stop+padding:], TextTypes.TEXT))

            # Add the results from the recursive call stack to the nodes
            nodes.extend(split_nodes_delimiter(chunks, delimiter, text_type))
        else:
            # This runs if the node is of type text but contains no delimiter
            nodes.append(node)

    return nodes

"""
    It does not do nesting and only parses TextNodes of type TextTypes.TEXT
"""
def split_nodes_image(old_nodes:list):
    nodes = list()
    for node in old_nodes:
        images = extract_markdown_images(node.text)

        if not node.text_type.name == TextTypes.TEXT.name:
            nodes.append(node)

        elif images:
            split_text = node.text.split(f"![{images[0][0]}]({images[0][1]})", 1)
            
            # Add the Text part before the first image
            if len(split_text[0]) > 1:
                nodes.append(
                    TextNode(split_text[0], TextTypes.TEXT)
                )
            # Add the first image
            nodes.append(
                TextNode(images[0][0], TextTypes.IMAGE, images[0][1])
            )
            # Parse the remainder of the text for images if there is any more text
            if len(split_text[1])> 1:
                nodes.extend(split_nodes_image([
                    TextNode(split_text[1], TextTypes.TEXT)
                ]))
        else:
            nodes.append(
                TextNode(node.text, TextTypes.TEXT)
            )

    return nodes
    
"""
    It does not do nesting and only parses TextNodes of type TextTypes.TEXT
"""
def split_nodes_links(old_nodes:list):
    nodes = list()
    
    for node in old_nodes:
        links = extract_markdown_links(node.text)

        if not node.text_type.name == TextTypes.TEXT.name:
            nodes.append(node)

        elif links:
            split_text = node.text.split(f"[{links[0][0]}]({links[0][1]})", 1)
            # Add the Text part before the first link
            if len(split_text[0]) > 1:
                nodes.append(
                    TextNode(split_text[0], TextTypes.TEXT)
                )
            # Add the first image
            nodes.append(
                TextNode(links[0][0], TextTypes.LINK, links[0][1])
            )
            # Parse the remainder of the text for links if there is any more text
            if len(split_text[1])> 1:
                nodes.extend(split_nodes_links([
                    TextNode(split_text[1], TextTypes.TEXT)
                ]))
        else:
            nodes.append(
                TextNode(node.text, TextTypes.TEXT)
            )

    return nodes

def text_to_nodes(text:str):
    nodes = [
        TextNode(text, TextTypes.TEXT)
    ]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_links(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextTypes.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextTypes.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextTypes.CODE)

    return nodes
