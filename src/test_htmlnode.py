import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_htmlnode1(self):
        node = HTMLNode("div", value="Hello World", children=[
            HTMLNode("p", value="This is a child node"),
            HTMLNode("p", value="This is another child node"),
            HTMLNode("p", value="This is yet another child node")
        ])
        node1 = HTMLNode("h1", value="Heading Node", props={"class": "heading", "id": "heading1", "data-test": "test"})
    
    
    def test_htmlnode2(self):
        node = HTMLNode("div", value="Hello World", children=[
            HTMLNode("p", value="This is a child node"),
            HTMLNode("p", value="This is another child node"),
            HTMLNode("p", value="This is yet another child node")
        ])
        node1 = HTMLNode("h1", value="Heading Node", props={"class": "heading", "id": "heading1", "data-test": "test"})
    
    
    def test_htmlnode3(self):
        node = HTMLNode("div", value="Hello World", children=[
            HTMLNode("p", value="This is a child node"),
            HTMLNode("p", value="This is another child node"),
            HTMLNode("p", value="This is yet another child node")
        ])
        node1 = HTMLNode("h1", value="Heading Node", props={"class": "heading", "id": "heading1", "data-test": "test"})