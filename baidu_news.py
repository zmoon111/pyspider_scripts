#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-08-05 08:00:08
# Project: baidunews

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=1 * 60)
    def on_start(self):
        self.crawl('http://news.baidu.com', callback=self.index_page)

    @config(age=60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
