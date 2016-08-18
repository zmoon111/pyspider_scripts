#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-08-08 07:18:17
# Project: baiduimage

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    """
    config, such as:cookie ...
    """
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        """
        first page to start, query='chinajoy'
        :return:
        """
        self.crawl('http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=chinajoy&oq=chinajoy&rsp=-1', fetch_type='js', js_script="""
                   function() {
                       setTimeout(window.scrollTo(0, document.body.scrollHeight), 5000);
                   }
                   """, callback=self.index_page)

    @config(age=60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http://image.baidu.com/search/detail"]').items():
            self.crawl(each.attr.href, fetch_type='js', callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        dir(response.doc('#srcPic>div>img').items())  //fetch image url by css selector
        return {
            "query": response.doc('#kw').attr('value'),
            "image_url": response.doc('#srcPic>div>img').attr('src'),
        }

