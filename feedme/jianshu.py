import requests
from html.parser import HTMLParser
from .util import Entry, Feed

HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; Feedme)'}


class JianshuParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super(JianshuParser, self).__init__(*args, **kwargs)
        self._process = None
        self._name = None
        self._items = []
        self._item = {}

    def handle_starttag(self, tag, attrs):
        params = dict(attrs)

        if tag == 'a' and params.get('class') == 'name':
            self._process = 'name'
            return

        if tag == 'a' and params.get('class') == 'blue-link':
            self._process = 'author'
        elif tag == 'span' and params.get('class') == 'time':
            self._process = None
            self._item['published'] = params.get('data-shared-at')
        elif tag == 'a' and params.get('class') == 'title':
            self._process = 'title'
            self._item['url'] = 'http://www.jianshu.com' + params.get('href')
        elif tag == 'p' and params.get('class') == 'abstract':
            self._process = 'content'
        else:
            self._process = None

    def handle_data(self, data):
        if self._process is not None:
            text = data.strip()
            if text:
                if self._process == 'name':
                    self._name = text
                    self._process = None
                else:
                    self._item[self._process] = text

    def handle_endtag(self, tag):
        if self._process == 'content':
            self._items.append(self._item)
            self._item = {}


def parse_jianshu_html(url):
    resp = requests.get(url, headers=HEADERS)
    p = JianshuParser()
    p.feed(resp.text)
    if not p._items:
        return None

    items = []
    for item in p._items:
        item['updated'] = item['published']
        items.append(Entry(**item))

    title = p._name
    return Feed(title=title, url=url, items=items)


def parse_jianshu_user(slug):
    url = 'http://www.jianshu.com/u/' + slug
    return parse_jianshu_html(url)


def parse_jianshu_column(slug):
    url = 'http://www.jianshu.com/c/' + slug
    return parse_jianshu_html(url)


def parse_jianshu_notebook(slug):
    url = 'http://www.jianshu.com/nb/' + slug
    return parse_jianshu_html(url)
