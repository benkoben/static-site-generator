import re

from enum import Enum
from leafnode import LeafNode

# I wanted to use Enums to learn more about the concept of sum types in python.
# This could have been solved in another way as well. What I like about this is the declaritive way of creating TextNodes.
# Any caller that imports the textnode module will easily understand the contraints they are working with in terms of choice of textTypes.
class TextTypes(Enum):
    TEXT = "text"
    BOLD = "b"
    ITALIC = "i"
    CODE = "code"
    LINK = "a"
    IMAGE = "img"

class TextNode():
    def __init__(self, text, text_type=None, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node) -> bool:
        if self.__repr__() == node.__repr__():
            return True
        return False
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
    def text_node_to_html_node(self):
        if self.text_type == TextTypes.TEXT:
            return LeafNode(
                value=self.text
            )
        if self.text_type == TextTypes.ITALIC or self.text_type == TextTypes.BOLD or self.text_type == TextTypes.CODE:
            return LeafNode(
                tag=self.text_type.value, 
                value=self.text
            )
        if self.text_type == TextTypes.LINK:
            return LeafNode(
                tag=self.text_type.value, 
                value=self.text,
                props={"href": self.url}
            )
        if self.text_type == TextTypes.IMAGE:
            return LeafNode(
                tag=self.text_type.value,
                props={"alt": self.text, "src": self.url} 
            )
        raise TypeError("invalid text type was used")