from htmlnode import HtmlNode

class LeafNode(HtmlNode):

    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("value cannot be None")
        super().__init__(tag=tag, value=value, props=props, children=None)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("value cannot be None")
        if self.tag is None:
            return self.value
        else:
            return self._tagger(self.value)
