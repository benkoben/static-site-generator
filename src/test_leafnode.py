import unittest

from leafnode import LeafNode 

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node1 = LeafNode(tag="a", value="this is a test link", props={"href": "https://www.example.com", "target": "_blank"})
        node2 = LeafNode(tag="a", value="this is a test link", props={"href": "https://www.example.com", "target": "_blank"})
        self.assertTrue(node1.__eq__(node2))

    def test_to_html_with_tags_and_props(self):
        node1 = LeafNode(tag="a", value="this is a test link", props={"href": "https://www.example.com", "target": "_blank"})
        nodeString1 = '<a href="https://www.example.com" target="_blank">this is a test link</a>'
        self.assertEqual(node1.to_html(), nodeString1)
        
    def test_to_html_with_value_only(self):
        node1 = LeafNode(tag=None, value="this is a test link", props={"href": "https://www.example.com", "target": "_blank"})
        nodeString1 = 'this is a test link'
        self.assertEqual(node1.to_html(), nodeString1)