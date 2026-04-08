import unittest
from generate_page import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_basic(self):
        # The standard case
        md = "# The Main Title"
        self.assertEqual(extract_title(md), "The Main Title")

    def test_extract_title_with_extra_whitespace(self):
        # Testing leading/trailing spaces within the h1 line
        md = "#    Title with Spaces   "
        self.assertEqual(extract_title(md), "Title with Spaces")

    def test_extract_title_multiline(self):
        # Ensuring it finds the title even if it's not the first line
        md = """
This is a intro paragraph.

# The Real Title

Other stuff.
"""
        self.assertEqual(extract_title(md), "The Real Title")

    def test_extract_title_no_h1(self):
        # Testing that it raises a ValueError when no h1 exists
        md = "## This is only an h2"
        with self.assertRaises(ValueError) as cm:
            extract_title(md)
        self.assertEqual(str(cm.exception), "Title not found in markdown content")

    def test_extract_title_missing_space(self):
        # Common markdown error: '#' without a space is technically not an h1
        md = "#TitleWithoutSpace"
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_extract_title_first_of_many(self):
        # If there are multiple h1s, it should return the first one found
        md = """
# First Title
# Second Title
"""
        self.assertEqual(extract_title(md), "First Title")

if __name__ == "__main__":
    unittest.main()