import unittest

from htmlnode import HTMLNode, LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("p", "Hello, world!", props={"class": "greeting", "id": "greeting1"})
        self.assertEqual(node.to_html(), '<p class="greeting" id="greeting1">Hello, world!</p>')

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_repr(self):
        node = LeafNode("p", "Hello, world!", props={"class": "greeting", "id": "greeting1"})
        self.assertEqual(repr(node), "LeafNode(tag=p, value=Hello, world!, props={'class': 'greeting', 'id': 'greeting1'})")



if __name__ == "__main__":
    unittest.main()