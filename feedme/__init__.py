from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map, Rule
from werkzeug.utils import redirect
from .util import render_feed
from .one import parse_one_feed
from .zhihu import parse_zhihu_zhuanlan, parse_zhihu_news
from .dajia import parse_dajia_author, parse_dajia_channel
from .jianshu import (
    parse_jianshu_user,
    parse_jianshu_column,
    parse_jianshu_notebook,
)


PARSERS = {
    'zhihu_zhuanlan': parse_zhihu_zhuanlan,
    'zhihu_news': parse_zhihu_news,
    'dajia_user': parse_dajia_author,
    'dajia_channel': parse_dajia_channel,
    'jianshu_user': parse_jianshu_user,
    'jianshu_column': parse_jianshu_column,
    'jianshu_notebook': parse_jianshu_notebook,
    'one_feed': parse_one_feed,
}


class Application(object):
    def __init__(self):
        self.url_map = Map([
            Rule('/', endpoint='home'),
            Rule('/zhihu/c/<slug>', endpoint='zhihu_zhuanlan'),
            Rule('/zhihu/n/<slug>', endpoint='zhihu_news'),
            Rule('/dajia/u/<slug>', endpoint='dajia_user'),
            Rule('/dajia/c/<slug>', endpoint='dajia_channel'),
            Rule('/jianshu/u/<slug>', endpoint='jianshu_user'),
            Rule('/jianshu/c/<slug>', endpoint='jianshu_column'),
            Rule('/jianshu/nb/<slug>', endpoint='jianshu_notebook'),
            Rule('/one/<slug>', endpoint='one_feed'),
        ])

    def _dispatch_request(self, environ):
        adapter = self.url_map.bind_to_environ(environ)
        try:
            endpoint, values = adapter.match()
            func = PARSERS.get(endpoint)
            if func:
                if 'slug' in values:
                    return render_feed(func(values['slug']))
                return render_feed(func())
            return redirect('https://github.com/lepture/feedme', 301)
        except HTTPException as e:
            return e

    def __call__(self, environ, start_response):
        response = self._dispatch_request(environ)
        return response(environ, start_response)
