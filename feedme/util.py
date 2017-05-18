from collections import namedtuple
from werkzeug.wrappers import Response
from werkzeug.exceptions import NotFound


Feed = namedtuple('Feed', ['title', 'url', 'items'])
Entry = namedtuple('Entry', [
    'title', 'url', 'author',
    'updated', 'published', 'content'
])

ENTRY_TPL = '''<entry>
<title><![CDATA[%(title)s]]></title>
<link href="%(url)s"/>
<id><![CDATA[%(url)s]]></id>
<author><name>%(author)s</name></author>
<updated>%(updated)s</updated>
<published>%(published)s</published>
<content type="html"><![CDATA[%(content)s]]></content>
</entry>
'''

FEED_HEAD = '''<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
<title><![CDATA[%(title)s]]></title>
<link href="%(url)s"/>
<id><![CDATA[%(url)s]]></id>
'''


def _iter_feed(feed):
    yield FEED_HEAD % feed._asdict()
    if feed.items:
        item = feed.items[0]
        yield '<updated>%s</updated>' % item.updated
        for item in feed.items:
            yield ENTRY_TPL % item._asdict()
    yield '</feed>'


def render_feed(feed):
    if feed is None:
        raise NotFound()
    return Response(_iter_feed(feed), content_type='text/xml; charset=utf-8')
