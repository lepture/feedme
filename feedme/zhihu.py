import datetime
import requests
from .util import Entry, Feed

BASE = 'https://zhuanlan.zhihu.com'
HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; Feedme)'}


def parse_zhihu_zhuanlan(slug):
    column_url = BASE + '/api/columns/' + slug

    posts_url = column_url + '/articles'
    resp = requests.get(posts_url, headers=HEADERS)
    if resp.status_code != 200:
        return None

    items = []
    for item in resp.json()['data']:
        title = item.get('title')
        url = item.get('url')
        content = item.get('excerpt')
        if title and url and content:
            author = item.get('author', {})
            items.append(Entry(
                title=title,
                url=url,
                updated=format_time(item.get('updated')),
                published=format_time(item.get('created')),
                content=content,
                author=author.get('name', '')
            ))

    resp = requests.get(column_url, headers=HEADERS)
    data = resp.json()
    title = data.get('title')
    url = data.get('url')
    return Feed(title=title, url=url, items=items)


def parse_zhihu_news(channel_id):
    url = 'https://news-at.zhihu.com/api/7/section/' + channel_id
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        return None

    data = resp.json()
    stories = data.get('stories')
    if not stories:
        return None

    items = []
    is_same_title = len({d['title'] for d in stories}) == 1

    for item in stories:
        date = item['date']
        published = '{}-{}-{}T00:00:00Z'.format(
            date[:4], date[4:6], date[6:8]
        )

        if is_same_title:
            title = item['display_date']
        else:
            title = item['title']

        content = '<h1>{}</h1>'.format(title)
        images = item.get('images')
        for src in images:
            content += '<img src="{}"/>'.format(src)

        items.append(Entry(
            title=title,
            url='https://daily.zhihu.com/story/{}'.format(item['id']),
            updated=published,
            published=published,
            content=content,
            author=''
        ))

    title = data['name']
    url = 'https://daily.zhihu.com/'
    return Feed(title=title, url=url, items=items)


def format_time(t):
    d = datetime.datetime.fromtimestamp(t)
    return d.strftime('%Y-%m-%dT%H:%M:%SZ')
