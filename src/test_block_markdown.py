import unittest

from block_markdown import markdown_to_blocks
from leafnode import LeafNode

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
            ['This is **bolded** paragraph'],
            ['This is another paragraph with *italic* text and `code` here', 'This is the same paragraph on a new line'],
            ['* This is a list', '* with items']
        ]
        self.assertEqual(markdown_to_blocks(test_case), expected_outcome)