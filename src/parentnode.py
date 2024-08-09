from htmlnode import HtmlNode

class ParentNode(HtmlNode):

    def __init__(self, tag=None, children=None, props=None):
        if children is None:
            raise ValueError("children must be provided")
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("must provide tag")
        if not self.children:
            raise ValueError("must provide children")
        
        content = "".join([c.to_html() for c in self.children])
        return self._tagger(content)