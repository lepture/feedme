from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map, Rule
from werkzeug.utils import redirect
from .util import render_feed
from .zhihu import parse_zhihu_zhuanlan, parse_zhihu_news
from .dajia import parse_dajia_author, parse_dajia_channel
from .jianshu import (
    parse_jianshu_user,
    parse_jianshu_column,
    parse_jianshu_notebook,
)


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
        ])

    def _dispatch_request(self, environ):
        adapter = self.url_map.bind_to_environ(environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, endpoint)(**values)
        except HTTPException as e:
            return e

    def __call__(self, environ, start_response):
        response = self._dispatch_request(environ)
        return response(environ, start_response)

    def home(self):
        return redirect('https://github.com/lepture/feedme', 301)

    def zhihu_zhuanlan(self, slug):
        return render_feed(parse_zhihu_zhuanlan(slug))

    def zhihu_news(self, slug):
        return render_feed(parse_zhihu_news(slug))

    def dajia_user(self, slug):
        return render_feed(parse_dajia_author(slug))

    def dajia_channel(self, slug):
        return render_feed(parse_dajia_channel(slug))

    def jianshu_user(self, slug):
        return render_feed(parse_jianshu_user(slug))

    def jianshu_column(self, slug):
        return render_feed(parse_jianshu_column(slug))

    def jianshu_notebook(self, slug):
        return render_feed(parse_jianshu_notebook(slug))
