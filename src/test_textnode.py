import unittest

from textnode import TextNode, TextTypes
from leafnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", "bold", "https//example.com/testnode")
        node2 = TextNode("This is a text node", "bold", "https//example.com/testnode")
        self.assertTrue(node1.__eq__(node2))

    def test_text_node_to_html_node(self):
        text_node = TextNode("This is a text node")
        bold_node = TextNode("This is a bold node", TextTypes.BOLD)
        italic_node = TextNode("This is an italic node", TextTypes.ITALIC)
        code_node = TextNode("This is a code node", TextTypes.CODE)
        link_node = TextNode("This is a link node", TextTypes.LINK, "https://example.com")
        image_node = TextNode("This is a image node", TextTypes.IMAGE, "https://example.image.com")
        invalid_node = TextNode("This is an invalid node", "invalid", "https://example.image.com")

        # assertions that check for successful operations
        self.assertEqual(text_node.text_node_to_html_node(), LeafNode(value="This is a text node"))
        self.assertEqual(bold_node.text_node_to_html_node(), LeafNode(tag="b", value="This is a bold node"))
        self.assertEqual(italic_node.text_node_to_html_node(), LeafNode(tag="i", value="This is an italic node"))
        self.assertEqual(code_node.text_node_to_html_node(), LeafNode(tag="code", value="This is a code node"))
        self.assertEqual(link_node.text_node_to_html_node(), LeafNode(tag="a", value="This is a link node", props={"href": "https://example.com"}))
        self.assertEqual(image_node.text_node_to_html_node(), LeafNode(tag="img", props={"alt": "This is a image node", "src": "https://example.image.com"}))
        
        # assertions that check for raised errors
        try:
            invalid_node.text_node_to_html_node()
        except TypeError as e:
            self.assertEqual(str(e), "invalid text type was used")
            


if __name__ == "__main__":
    unittest.main()