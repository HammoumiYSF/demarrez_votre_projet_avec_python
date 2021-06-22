# -*- coding: utf-8 -*-
import scrapy
import html
import unicodedata

class BlogSpider(scrapy.Spider):
    name = 'characterspider'
    start_urls = ['https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Personnage_d\'animation']

    def parse(self, response):
        for link in response.css('div#mw-pages div.mw-content-ltr li'):
            character = link.css('a ::text').extract_first()
            decoded = html.unescape(character)
            char = unicodedata.normalize('NFD', decoded).encode('ascii', 'ignore').decode("utf-8")
            yield {'character':char}