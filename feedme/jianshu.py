import requests
from bs4 import BeautifulSoup
from .util import Entry, Feed

HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; Feedme)'}


def parse_jianshu_html(url):
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')
    titles = soup.select('div.title a.name')
    if not titles:
        return None
    title = titles[0].get_text()

    items = []
    for el in soup.select('ul.note-list li'):
        item = {}
        author = el.find('a', class_='blue-link')
        if author:
            item['author'] = author.get_text().strip()
        updated = el.find('span', class_='time')
        if updated:
            item['updated'] = updated.get('data-shared-at')
            item['published'] = item['updated']
        el_title = el.find('a', class_='title')
        if el_title:
            item['title'] = el_title.get_text().strip()
            item['url'] = 'http://www.jianshu.com' + el_title.get('href')
        content = el.find('p', class_='abstract')
        if content:
            item['content'] = content.get_text().strip()
        items.append(Entry(**item))
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
