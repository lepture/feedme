import re
import requests
from .util import Entry, Feed

TITLE_SUFFIX = u' - 「ONE · 一个」'
TITLE_MAP = {
    'article': u'阅读',
    'movie': u'影视',
    'music': u'音乐',
}
BASE_URL = 'http://m.wufazhuce.com/'
TOKEN_URL = 'http://m.wufazhuce.com/article'
TOKEN_PATTERN = re.compile(r"One\.token = '(.*?)';")
API_URL = 'http://m.wufazhuce.com/article/ajaxlist/0'
HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; Feedme)'}


def parse_one_feed(category):
    title_prefix = TITLE_MAP.get(category)
    if not title_prefix:
        return None

    url = BASE_URL + category
    sess = requests.Session()
    resp = sess.get(url, headers=HEADERS)
    m = TOKEN_PATTERN.findall(resp.text)

    api_url = 'http://m.wufazhuce.com/{}/ajaxlist/0'.format(category)
    resp = sess.get(api_url, params={'_token': m[0]}, headers=HEADERS)
    result = resp.json()
    items = list(format_entries(result['data']))
    title = title_prefix + TITLE_SUFFIX
    return Feed(title=title, url=url, items=items)


def format_entries(entries):
    for item in entries:
        updated = _format_time(item['last_update_date'])
        published = _format_time(item['post_date'])
        yield Entry(
            title=item['title'],
            url=item['url'],
            updated=updated,
            published=published,
            content=item['forward'],
            author=item['author']['user_name'],
        )


def _format_time(s):
    return s.replace(' ', 'T') + '+08:00'
