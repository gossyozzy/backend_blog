from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    URL = "url"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type = TextType, url = None)
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        text_eq = self.text == other.text
        text_type_eq = self.text_type == other.text_type
        url_eq = self.url == other.url

        if text_eq and text_type_eq and url_eq:
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url}"
