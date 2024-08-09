
class HtmlNode(object):
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if isinstance(self.props, dict):
            return " " + " ".join([f'{k}="{v}"' for k, v in self.props.items()])
        else:
            return ""

    def _tagger(self, content):
        return f'<{self.tag}{self.props_to_html()}>{content}</{self.tag}>'
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.tag}, {self.value}, {self.children}, {self.props})'