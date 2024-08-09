
class TextNode(object):

    def __init__(self, text, text_type="", url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        text_same = self.text == other.text
        type_same = self.text_type == other.text_type
        url_same = (self.url is None and other.url is None) or (self.url == other.url)

        return text_same and type_same and url_same

    def __repr__(self):
        if self.url is None:
            return f'{self.__class__.__name__}("{self.text}", "{self.text_type}", None)'
        else:
            return f'{self.__class__.__name__}("{self.text}", "{self.text_type}", "{self.url}")'