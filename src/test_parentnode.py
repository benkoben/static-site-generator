import unittest

from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_nesting(self):
        # Should not fail
        node_without_errors = ParentNode(
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
        self.assertEqual(
            node_without_errors.to_html(), 
            "<p><b>Bold text</b>Normal text<th><td>table data</td><td>table data</td></th><i>italic text</i>Normal text</p>"
        )

    def test_children(self):
        # Should fail
        node_with_empty_children = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                    "th",
                    [],
                    ),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        try:
            node_with_empty_children.to_html()
        except ValueError as e:
            self.assertEqual(str(e), "children cannot be None" )

        # Should fail
        node_with_none_children = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                    "th",
                    None,
                    ),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        try:
            node_with_none_children.to_html()
        except ValueError as e:
            self.assertEqual(str(e), "children cannot be None" )

    def test_tag(self):
        # Should fail
        node_with_none_tag = ParentNode(
            None,
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                    None,
                    [
                        LeafNode("td", "table data"),
                        LeafNode("td", "table data"),
                    ],
                    ),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        try:
            node_with_none_tag.to_html()
        except ValueError as e:
            self.assertEqual(str(e), "tag cannot be None" )
        # Should fail
        node_with_empty_tag = ParentNode(
            "",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                    None,
                    [
                        LeafNode("td", "table data"),
                        LeafNode("td", "table data"),
                    ],
                    ),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        try:
            node_with_empty_tag.to_html()
        except ValueError as e:
            self.assertEqual(str(e), "tag cannot be None" )