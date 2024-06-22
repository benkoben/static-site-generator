from htmlnode import HtmlNode

class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("tag cannot be None")

        if not self.children:
            raise ValueError("children cannot be None")
        
        html = f"<{self.tag}>"
        for child in self.children:
            if child != self.children[-1]:
                html += child.to_html() + "\n"
            else:
                html += child.to_html()

        html += f"</{self.tag}>"
        return html