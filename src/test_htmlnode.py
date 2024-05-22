import unittest

from htmlnode import HtmlNode

class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node1 = HtmlNode("a", "this is a link", None, {"href": "https://www.google.com", "target": "_blank"})
        node2 = HtmlNode("a", "this is a link", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertTrue(node1.__eq__(node2))
        
        prop1 = node1.props_to_html()
        prop2 = node2.props_to_html()
        self.assertTrue(prop1.__eq__(prop2))

if __name__ == "__main__":
    unittest.main()