#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-08-18 08:34:42
# Project: taomm

from pyspider.libs.base_handler import *
import re


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://mm.taobao.com/search_tstar_model.htm?spm=719.1001036.1998606017.2.2BHsy4', fetch_type='js', js_script="""
                   function() {
                       setTimeout(window.scrollTo(0, document.body.scrollHeight), 2000);
                   }
                   """, callback=self.index_page)

    @config(age=60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match("https://mm.taobao.com/self/aiShow.htm", each.attr.href):
                self.crawl(each.attr.href, fetch_type='js', js_script="""
                   function() {
                       setTimeout(window.scrollTo(0, document.body.scrollHeight), 2000);
                   }
                   """, callback=self.detail_page)
    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
            "image_url" : response.doc('img').attr.src
        }

