#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-08-09 09:18:34
# Project: huaban

from pyspider.libs.base_handler import *
import re


class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'itag': 'v5',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        }
    }

    @every(minutes=12 * 60)
    def on_start(self):
        self.crawl('http://huaban.com/favorite/quotes/',
                   fetch_type='js', js_script="""
                   function() {
                       setTimeout(window.scrollTo(0, document.body.scrollHeight), 2000);
                   }
                   """, callback=self.index_page)

    @config(age=60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match("http://huaban.com/pins/\d+/$", each.attr.href):
                self.crawl(each.attr.href, fetch_type='js', callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "title": response.doc('title').text(),
            "image_url" : response.doc('div > img').attr.src,
            "image_desc" : response.doc('div > img').attr.alt
        }
