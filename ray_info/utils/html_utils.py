from io import StringIO
from html.parser import HTMLParser
from urllib.parse import urlparse
import os

def url_to_file_name(url: str):
    return os.path.basename(urlparse(url).path)

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html, limit=None):
    s = MLStripper()
    s.feed(html)
    if limit:
        return s.get_data()[:limit]
    else:
        return s.get_data()
