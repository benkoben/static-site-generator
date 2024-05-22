from htmlnode import HtmlNode

class LeafNode(HtmlNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    
    def to_html(self):
        if not self.value:
            raise ValueError("value cannot be None")
        html = f"{self.value}"
        if self.tag:
            props = super().props_to_html()
            html = f"<{self.tag}{props}>" + html + f"</{self.tag}>" 
        return html

    def __eq__(self, node) -> bool:
        if self.__repr__() == node.__repr__():
            return True
        return False
    
    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"