import unittest

from textnode import TextNode, TextTypes, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_links, text_to_nodes
from leafnode import LeafNode

class TestTextNode(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.maxDiff = None

    def test_eq(self):
        node1 = TextNode("This is a text node", "bold", "https//example.com/testnode")
        node2 = TextNode("This is a text node", "bold", "https//example.com/testnode")
        self.assertTrue(node1.__eq__(node2))

    def test_text_node_to_html_node(self):
        text_node = TextNode("This is a text node", TextTypes.TEXT)
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

    def test_split_nodes_delimiter(self):
        # Test code blocks
        test1 = {
            "input": [TextNode("This is text with a `code block` and then another `code block`. The end :)", TextTypes.TEXT)],
            "expected_output": [
                TextNode("This is text with a ", TextTypes.TEXT, None),
                TextNode("code block", TextTypes.CODE, None),
                TextNode(" and then another ", TextTypes.TEXT, None),
                TextNode("code block", TextTypes.CODE, None),
                TextNode(". The end :)", TextTypes.TEXT, None)
            ]
        }
        self.assertEqual(
            split_nodes_delimiter(
                test1["input"], "`", TextTypes.CODE), 
                test1["expected_output"]
            )
        # Test italic blocks
        test2 = {
            "input": [TextNode("This is text with a *italic block* and then another *italic block*. The end :)", TextTypes.TEXT)],
            "expected_output": [
                TextNode("This is text with a ", TextTypes.TEXT, None),
                TextNode("italic block", TextTypes.ITALIC, None),
                TextNode(" and then another ", TextTypes.TEXT, None),
                TextNode("italic block", TextTypes.ITALIC, None),
                TextNode(". The end :)", TextTypes.TEXT, None)
            ]
        }
        self.assertEqual(
            split_nodes_delimiter(
                test2["input"], "*", TextTypes.ITALIC), 
                test2["expected_output"]
            )
        # Test bold blocks
        test3 = {
            "input": [TextNode("This is text with a **bold block** and then another **bold block**. The end :)", TextTypes.TEXT)],
            "expected_output": [
                TextNode("This is text with a ", TextTypes.TEXT, None),
                TextNode("bold block", TextTypes.BOLD, None),
                TextNode(" and then another ", TextTypes.TEXT, None),
                TextNode("bold block", TextTypes.BOLD, None),
                TextNode(". The end :)", TextTypes.TEXT, None)
            ]
        }
        self.assertEqual(
            split_nodes_delimiter(
                test3["input"], "**", TextTypes.BOLD), 
                test3["expected_output"]
            )
        
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        self.assertEqual(extract_markdown_images(text), [
            ('image','https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png'),
            ('another','https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png')
        ])

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual(extract_markdown_links(text), [
            ('link', 'https://www.example.com'),
            ('another', 'https://www.example.com/another')
        ])


    def test_split_nodes_image(self):
        image_text = [TextNode("This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png) and then some trailing text", TextTypes.TEXT)]
        self.assertEqual(split_nodes_image(image_text), [
            TextNode("This is text with an ", TextTypes.TEXT, None),
            TextNode("image", TextTypes.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and ", TextTypes.TEXT, None),
            TextNode("another", TextTypes.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png"),
            TextNode(" and then some trailing text", TextTypes.TEXT, None),
        ])

    def test_split_nodes_link(self):
        link_text = [TextNode('This is text with a [link](https://www.example.com) and [another](https://www.example.com/another) and then some text', TextTypes.TEXT)]
        self.assertEqual(split_nodes_links(link_text), [
            TextNode("This is text with a ", TextTypes.TEXT, None),
            TextNode("link", TextTypes.LINK, "https://www.example.com"),
            TextNode(" and ", TextTypes.TEXT, None),
            TextNode("another", TextTypes.LINK, "https://www.example.com/another"),
            TextNode(" and then some text", TextTypes.TEXT, None),
        ])

    def test_text_to_nodes(self):
        test_case = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        expected_outcome = [
            TextNode("This is ", TextTypes.TEXT, None),
            TextNode("text", TextTypes.BOLD, None),
            TextNode(" with an ", TextTypes.TEXT, None),
            TextNode("italic", TextTypes.ITALIC, None),
            TextNode(" word and a ", TextTypes.TEXT, None),
            TextNode("code block", TextTypes.CODE, None),
            TextNode(" and an ", TextTypes.TEXT, None),
            TextNode("image", TextTypes.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", TextTypes.TEXT, None),
            TextNode("link", TextTypes.LINK, "https://boot.dev"),
        ]
        self.assertEqual(
            text_to_nodes(test_case),
            expected_outcome
        )

if __name__ == "__main__":
    unittest.main()