import time
import requests
from .util import Entry, Feed

REFERRER = 'http://dajia.qq.com/author_personal.htm'
WZ_URL = 'http://i.match.qq.com/ninjayc/dajiawenzhanglist'
CHANNEL_URL = 'http://i.match.qq.com/ninjayc/dajialanmu'
USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36'
)


def parse_dajia_author(author_id):
    headers = {'User-Agent': USER_AGENT, 'Referer': REFERRER}
    t = int(time.time())

    params = {'action': 'wz', 'authorid': author_id, '_': t}
    resp = requests.get(WZ_URL, headers=headers, params=params)
    if resp.status_code != 200:
        return None

    data = resp.json()
    entries = data.get('data')
    if not entries:
        return None

    latest = entries[0]
    author = latest.get('name')
    url = 'http://dajia.qq.com/author_personal.htm#!/' + author_id

    items = list(format_entries(entries))
    return Feed(title=author, url=url, items=items)


def parse_dajia_channel(channel_id):
    headers = {'User-Agent': USER_AGENT, 'Referer': REFERRER}
    t = int(time.time())

    params = {'action': 'wz', 'channelid': channel_id, '_': t}
    resp = requests.get(WZ_URL, headers=headers, params=params)
    if resp.status_code != 200:
        return None

    data = resp.json()
    entries = data.get('data')
    if not entries:
        return None

    params = {'action': 'lanmu', 'channelid': channel_id, '_': t}
    resp = requests.get(CHANNEL_URL, headers=headers, params=params)
    data = resp.json()
    title = data['data']['channel']['n_cname']
    url = 'http://dajia.qq.com/tanzi_diceng.htm#!/' + channel_id
    items = list(format_entries(entries))
    return Feed(title=title, url=url, items=items)


def format_entries(entries):
    for item in entries:
        published = item['n_publishtime']
        published = published.replace(' ', 'T') + '+08:00'
        yield Entry(
            title=item['n_title'],
            url=item['n_url'],
            updated=published,
            published=published,
            content=item['n_describe'],
            author=item['name'],
        )
