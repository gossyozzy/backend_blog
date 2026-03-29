import unittest
from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,

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

class TestImageSplitter(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_none(self):
        node = TextNode("Just some plain text here.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("Just some plain text here.", TextType.TEXT)],
            new_nodes
    )

    def test_split_image_at_start(self):
        node = TextNode("![alt](https://url.com) and then text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("alt", TextType.IMAGE, "https://url.com"),
                TextNode(" and then text", TextType.TEXT),
            ],
            new_nodes
        )

    def test_split_images_consecutive(self):
        node = TextNode("![first](url1)![second](url2)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "url1"),
                TextNode("second", TextType.IMAGE, "url2"),
            ],
            new_nodes
        )

    def test_split_images_mixed_nodes(self):
        node1 = TextNode("Image: ![alt](url)", TextType.TEXT)
        node2 = TextNode("I am already an image", TextType.IMAGE, "url2")
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("Image: ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "url"),
                TextNode("I am already an image", TextType.IMAGE, "url2"),
            ],
            new_nodes
        )

    def test_split_image_at_end(self):
        node = TextNode("This ends with an ![image](https://url.com/img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This ends with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://url.com/img.png"),
            ],
            new_nodes
        )


class TestLinkSplitter(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.URL, "https://boot.dev"),
                # Note the space and punctuation preserved here
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.URL, "https://blog.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_link_at_start(self):
        node = TextNode("[Click here](https://google.com) to search.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Click here", TextType.URL, "https://google.com"),
                TextNode(" to search.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_at_end(self):
        node = TextNode("Follow me on [Twitter](https://twitter.com/bootdev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Follow me on ", TextType.TEXT),
                TextNode("Twitter", TextType.URL, "https://twitter.com/bootdev"),
            ],
            new_nodes,
        )

    def test_split_links_consecutive(self):
        node = TextNode("[one](url1)[two](url2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("one", TextType.URL, "url1"),
                TextNode("two", TextType.URL, "url2"),
            ],
            new_nodes,
        )

    def test_split_links_none(self):
        node = TextNode("This is just a sentence with no links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is just a sentence with no links.", TextType.TEXT)],
            new_nodes
        )

    def test_split_links_ignores_images(self):
        node = TextNode(
            "This is a [link](url1) and an ![image](url2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.URL, "url1"),
                TextNode(" and an ![image](url2)", TextType.TEXT),
            ],
            new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **bold** and _italic_ and `code` and an ![image](url) and a [link](url)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.URL, "url"),
        ]
        self.assertListEqual(expected, text_to_textnodes(text))

    def test_text_to_textnodes_text_only(self):
        text = "This is plain old text with no formatting."
        expected = [
            TextNode("This is plain old text with no formatting.", TextType.TEXT),
        ]
        self.assertListEqual(expected, text_to_textnodes(text))

    def test_text_to_textnodes_empty(self):
        text = ""
        expected = []
        self.assertListEqual(expected, text_to_textnodes(text))

    def test_text_to_textnodes_image_first(self):
        text = "![The image here is first](url) followed by some other text."
        expected = [
            TextNode("The image here is first", TextType.IMAGE, "url"),
            TextNode(" followed by some other text.", TextType.TEXT),
        ]
        self.assertListEqual(expected, text_to_textnodes(text))


    def test_text_to_textnodes_bold_only(self):
        text = "**This is bold text only.**"
        expected = [
            TextNode("This is bold text only.", TextType.BOLD),
        ]
        self.assertListEqual(expected, text_to_textnodes(text))


if __name__ == "__main__":
    unittest.main()