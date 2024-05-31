def markdown_to_blocks(text):
    blocks = list()
    for block in text.lstrip("\n").rstrip("\n").split("\n\n"):
        blocks.append(block.split("\n"))
    return blocks
