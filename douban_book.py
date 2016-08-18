#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-08-09 08:58:16
# Project: doubanbook

from pyspider.libs.base_handler import *
import re


class Handler(BaseHandler):
    crawl_config = {
     'itag': 'v2'
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://book.douban.com/chart?icn=index-topchart-nonfiction', callback=self.index_page)

    @config(age=60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match("https://book.douban.com/subject/\d+/$", each.attr.href):
                self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        response.doc('#mainpic>a>img').attr.src
        return {
            "title": response.doc('title').text(),
            "book_image":  response.doc('#mainpic>a>img').attr.src,
            "book_name": response.doc('#wrapper>h1>span').text(),
            "score" : response.doc('#interest_sectl>div>div.rating_self.clearfix>strong').text()
        }
