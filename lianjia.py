#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-08-08 06:12:55
# Project: lianjia

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://bj.lianjia.com/zufang/rs%E4%B8%AD%E5%85%B3%E6%9D%91/', callback=self.index_page)

    @config(age=60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
