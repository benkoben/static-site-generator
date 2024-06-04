import unittest

from block_markdown import markdown_to_blocks, block_to_block_type, BlockTypes, header_block_to_html, code_block_to_html
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextTypes

class TestTextNode(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_markdown_to_blocks(self):
        test_case = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        expected_outcome = [
            'This is **bolded** paragraph',
            'This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line',
            '* This is a list\n* with items'
        ]
        self.assertEqual(markdown_to_blocks(test_case), expected_outcome)


    def test_block_to_block_type(self):
        header_test_1 = "# This is a h1 header"
        header_test_2 = "## This is a h2 header"
        header_test_3 = "### This is a h3 header"
        header_test_4 = "#### This is a h4 header"
        header_test_5 = "##### This is a h5 header"
        header_test_6 = "###### This is a h6 header"
        header_test_7 = "######This is an invalid header"
        header_test_8 = "####### This is an invalid header"
        
        code_test_1 = "```python\nprint('hello world')\n```"
        # invalid
        code_test_2 = "```python\nprint('hello world')\nmissing closing backtics"

        quote_test_1 = "> this is quoted\n> continuing the quote"
        # invalid
        quote_test_2 = "> this is quoted\nbreaking the quote with this line"

        unordered_list_test_1 = "* line 1\n* line2\n* line 3\n* line 4"
        # invalid
        unordered_list_test_2 = "* line 1\n* line2\n line 3\n line 4"

        ordered_list_test_1 = "1. line 1\n2. line two\n3. line three"
        # invalid
        ordered_list_test_2 = "1. line 1\n line two\n3. line three"
        
        # First test all valid cases
        #
        # Headers
        self.assertEqual(block_to_block_type(header_test_1), BlockTypes.HEADING)
        self.assertEqual(block_to_block_type(header_test_2), BlockTypes.HEADING)
        self.assertEqual(block_to_block_type(header_test_3), BlockTypes.HEADING)
        self.assertEqual(block_to_block_type(header_test_4), BlockTypes.HEADING)
        self.assertEqual(block_to_block_type(header_test_5), BlockTypes.HEADING)
        self.assertEqual(block_to_block_type(header_test_6), BlockTypes.HEADING)
        # Code blocks
        self.assertEqual(block_to_block_type(code_test_1), BlockTypes.CODE)
        # Quote blocks
        self.assertEqual(block_to_block_type(quote_test_1), BlockTypes.QUOTE)
        # Unordered list blocks
        self.assertEqual(block_to_block_type(unordered_list_test_1), BlockTypes.UNORDERED_LIST)
        # Ordered list blocks 
        self.assertEqual(block_to_block_type(ordered_list_test_1), BlockTypes.ORDERED_LIST)

        # Check to see if invalid cases default to BlockTypes.PARAGRAPH
        self.assertEqual(block_to_block_type(header_test_7), BlockTypes.PARAGRAPH)
        self.assertEqual(block_to_block_type(header_test_8), BlockTypes.PARAGRAPH)
        self.assertEqual(block_to_block_type(code_test_2), BlockTypes.PARAGRAPH)
        self.assertEqual(block_to_block_type(quote_test_2), BlockTypes.PARAGRAPH)
        self.assertEqual(block_to_block_type(unordered_list_test_2), BlockTypes.PARAGRAPH)
        self.assertEqual(block_to_block_type(ordered_list_test_2), BlockTypes.PARAGRAPH)

    def test_header_block_to_html(self):
        header_test_1 = "# This is a h1 header"
        header_test_2 = "## This is a h2 header"
        header_test_3 = "### This is a h3 header"
        header_test_4 = "#### This is a h4 header"
        header_test_5 = "##### This is a h5 header"
        header_test_6 = "###### This is a h6 header"
        header_test_7 = "######This is an invalid header"
        header_test_8 = "####### This is an invalid header"
        header_test_9 = "This is an invalid header"

        code_test_1 = "```python\nprint('hello world')\n```"
        expected_code_test_1_output = ParentNode("pre", ParentNode("code", [
            TextNode("print('hello world')", TextTypes.TEXT)
        ]))
        # invalid
        code_test_2 = "```python\nprint('hello world')\nmissing closing backtics"

        # Assert valid cases
        self.assertEqual(header_block_to_html(header_test_1), LeafNode("h1", "This is a h1 header"))
        self.assertEqual(header_block_to_html(header_test_2), LeafNode("h2", "This is a h2 header"))
        self.assertEqual(header_block_to_html(header_test_3), LeafNode("h3", "This is a h3 header"))
        self.assertEqual(header_block_to_html(header_test_4), LeafNode("h4", "This is a h4 header"))
        self.assertEqual(header_block_to_html(header_test_5), LeafNode("h5", "This is a h5 header"))
        self.assertEqual(header_block_to_html(header_test_6), LeafNode("h6", "This is a h6 header"))

        # Assert invalid cases
        for test in [header_test_7, header_test_8, header_test_9]:
            try:
                header_block_to_html(test)
            except ValueError as e:
                self.assertEqual(str(e), "header_block does not contain a valid markdown header")

        self.assertEqual(code_block_to_html(code_test_1), expected_code_test_1_output)