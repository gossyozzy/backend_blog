import unittest
from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


class TestMarkdownExtractor(unittest.TestCase):

    def test_single_image(self):
        text = "Here is an ![alt text](https://link.com/img.png)"
        expected = [("alt text", "https://link.com/img.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_multiple_images(self):
        text = "![one](url1) and ![two](url2)"
        expected = [("one", "url1"), ("two", "url2")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_no_images(self):
        text = "This is just plain text with no images."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_standard_link_ignored(self):
        # Images start with !, links do not. This ensures we don't grab links.
        text = "This is a [link](https://google.com), not an image."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_empty_alt_text(self):
        text = "An image with no alt: ![](https://link.com/img.png)"
        expected = [("", "https://link.com/img.png")]
        self.assertEqual(extract_markdown_images(text), expected)

class TestLinkExtractor(unittest.TestCase):

    def test_standard_link(self):
        text = "Check out [Google](https://google.com)"
        expected = [("Google", "https://google.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multiple_links(self):
        text = "[Link 1](url1) and [Link 2](url2)"
        expected = [("Link 1", "url1"), ("Link 2", "url2")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_ignores_images(self):
        # This is the most important test for your specific regex!
        text = "This is a ![image](img_url) and this is a [link](link_url)"
        expected = [("link", "link_url")]
        self.assertEqual(extract_markdown_links(text), expected, "Should ignore images starting with '!'")

    def test_link_at_start_of_string(self):
        # Lookbehinds can sometimes be finicky at the very start of a string
        text = "[Start](https://start.com) of the sentence."
        expected = [("Start", "https://start.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_no_links(self):
        text = "Just some text with an ![image](img_url) and no links."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_empty_link_text(self):
        text = "Click [](https://anonymous.com)"
        expected = [("", "https://anonymous.com")]
        self.assertEqual(extract_markdown_links(text), expected)


if __name__ == "__main__":
    unittest.main()