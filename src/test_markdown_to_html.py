import unittest
from markdown_to_html import markdown_to_html


class TestMarkdownToHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


    def test_headings(self):
        md = """
# This is an h1

## This is an h2 with **bold**
"""
        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is an h1</h1><h2>This is an h2 with <b>bold</b></h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a quote
> that spans multiple lines
"""
        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote that spans multiple lines</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- First item
- Second item with _italics_
- Third item
"""
        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item with <i>italics</i></li><li>Third item</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item
"""
        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li></ol></div>",
        )

    def test_mixed_blocks(self):
        md = """
# Heading

This is a paragraph.

- List item 1
- List item 2
"""
        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading</h1><p>This is a paragraph.</p><ul><li>List item 1</li><li>List item 2</li></ul></div>",
        )




if __name__ == "__main__":
    unittest.main()