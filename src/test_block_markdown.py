import unittest

from block_markdown import *
from block import *


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

    def test_markdown_to_blocks_basic(self):
        # Standard case: two paragraphs separated by double newlines
        md = "This is the first block.\n\nThis is the second block."
        expected = ["This is the first block.", "This is the second block."]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_markdown_to_blocks_mixed_types(self):
        # Testing different markdown elements (header and list)
        md = "# This is a heading\n\n* This is a list item\n* This is another"
        expected = [
            "# This is a heading",
            "* This is a list item\n* This is another"
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_markdown_to_blocks_extra_newlines(self):
        # Testing more than two newlines between blocks
        md = "Block 1\n\n\n\nBlock 2"
        expected = ["Block 1", "Block 2"]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_markdown_to_blocks_whitespace_handling(self):
        # Testing leading/trailing whitespace and extra newlines at the ends
        md = "   \n\n# Heading   \n\nParagraph text here. \n\n   "
        expected = ["# Heading", "Paragraph text here."]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_markdown_to_blocks_single_block(self):
        # Testing a single line of text
        md = "Just one block of text."
        expected = ["Just one block of text."]
        self.assertEqual(markdown_to_blocks(md), expected)



class TestBlockToBlockType(unittest.TestCase):

    def test_paragraph(self):
        self.assertEqual(BlockType.block_to_block_type("Just a normal paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(BlockType.block_to_block_type(""), BlockType.PARAGRAPH)

    def test_heading(self):
        self.assertEqual(BlockType.block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(BlockType.block_to_block_type("###### Heading 6"), BlockType.HEADING)
        # Should be a paragraph if there are 7 hashes or no space
        self.assertEqual(BlockType.block_to_block_type("####### Too many hashes"), BlockType.PARAGRAPH)
        self.assertEqual(BlockType.block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    def test_code_block(self):
        code = "```\nprint('hello')\n```"
        self.assertEqual(BlockType.block_to_block_type(code), BlockType.CODE)
        # Fail if missing the newline after the backticks
        self.assertEqual(BlockType.block_to_block_type("```print('hello')```"), BlockType.PARAGRAPH)

    def test_quote_block(self):
        quote = "> Line 1\n> Line 2\n> Line 3"
        self.assertEqual(BlockType.block_to_block_type(quote), BlockType.QUOTE)
        # Fail if one line is missing the symbol
        bad_quote = "> Line 1\nLine 2"
        self.assertEqual(BlockType.block_to_block_type(bad_quote), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        ul = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(BlockType.block_to_block_type(ul), BlockType.UNORDERED_LIST)
        # Fail if using * instead of -
        self.assertEqual(BlockType.block_to_block_type("* Item 1"), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        ol = "1. First\n2. Second\n3. Third"
        self.assertEqual(BlockType.block_to_block_type(ol), BlockType.ORDERED_LIST)
        
    def test_ordered_list_failures(self):
        # Starts at 2 instead of 1
        self.assertEqual(BlockType.block_to_block_type("2. Start at two"), BlockType.PARAGRAPH)
        # Skips a number
        bad_seq = "1. First\n3. Third"
        self.assertEqual(BlockType.block_to_block_type(bad_seq), BlockType.PARAGRAPH)
        # Missing the space or period
        self.assertEqual(BlockType.block_to_block_type("1 First"), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()