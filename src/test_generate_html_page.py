import unittest

from generate_html_page import *

class TestGenerateHtml(unittest.TestCase):

    def test_extract_title(self):
        test_case_1 = """
# This is a title

And the is a paragraph
with multiple lines.
"""
        expected_outcome_1 = "This is a title"

        test_case_2 = """
## This is a faulty title

And the is a paragraph
with multiple lines.
"""
        expected_outcome_2 = "markdown invalid. make sure the first block in markdown does start with \"# \""

        test_case_3 = """
> This is another faulty title

And the is a paragraph
with multiple lines.
"""
        expected_outcome_3 = "markdown invalid. make sure the first block in markdown does start with \"# \""

        test_case_4 = ""
        expected_outcome_4 = "markdown cannot be an empty string"

        self.assertEqual(extract_title(test_case_1), expected_outcome_1)

        for case, expected in zip([test_case_2, test_case_3, test_case_4], [expected_outcome_2, expected_outcome_3, expected_outcome_4]):
            try:
                extract_title(case)
            except ValueError as e:
                self.assertEqual(str(e), expected)

if __name__ == "__main__":
    unittest.main()