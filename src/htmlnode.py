class HtmlNode():
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None:
            return ""

        html = ""
        for k,v in self.props.items():
            html += f' {k}="{v}"'
        return html

    def __eq__(self, node) -> bool:
        if self.__repr__() == node.__repr__():
            return True
        return False

    def __repr__(self) -> str:
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"
