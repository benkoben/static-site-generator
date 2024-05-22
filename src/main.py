from textnode import TextNode, TextTypes
from leafnode import LeafNode
from parentnode import ParentNode

def main():
    text_node = TextNode(
        text="This is just a dummy textNode",
        text_type="bold",
        url="https://example.com/textnode"
    )

    print(text_node.__repr__())

    leaf_node = LeafNode(
        tag="h1",
        value="header",
        props={"href": "https://www.example.com", "target": "_blank"}
    )

    print(leaf_node.to_html())  

    node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        ParentNode(
            "th",
            [
                LeafNode("td", "table data"),
                LeafNode("td", "table data"),
            ],
            ),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
    )

    print(node.to_html())

    text_node = TextNode("This is a text node")
    print(TextTypes.BOLD.value)

if __name__ == "__main__":
    main()