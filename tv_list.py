#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-01-04 03:26:04
# Project: tutorial_twitch

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    """
    This is a sample script for: Level 2: AJAX and More HTTP and Level 3: Render with PhantomJS
    http://docs.pyspider.org/en/latest/tutorial/AJAX-and-more-HTTP/#ajax
    http://docs.pyspider.org/en/latest/tutorial/Render-with-PhantomJS/#use-phantomjs
    """
    @every(minutes=10)
    def on_start(self):
        self.crawl('http://api.twitch.tv/kraken/streams?limit=20&offset=0&game=Dota+2&broadcaster_language=&on_site=1',
                   callback=self.parse_json)
        self.crawl('http://www.twitch.tv/directory/game/Dota%202',
                   fetch_type='js', callback=self.parse_rendered_page)

    @config(age=10*60)
    def parse_json(self, response):
        """
        directly call json api, and parse result, you should find it before
        :param response:
        :return:
        """
        return [{
                "name": x['channel']['display_name'],
                "viewers": x['viewers'],
                "status": x['channel'].get('status'),
             } for x in response.json['streams']]

    @config(age=10*60)
    def parse_rendered_page(self, response):
        return {
            "url": response.url,
            "channels": [{
                "title": x('.title').text(),
                "viewers": x('.info').contents()[2],
                "name": x('.info a').text(),
            } for x in response.doc('.stream.item').items()]
        }