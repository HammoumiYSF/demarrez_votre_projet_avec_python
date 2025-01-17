# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import html
import unicodedata

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['http://www.babelio.com/auteur/Frederic-Dard/7187/citations']

    def parse(self, response):
        for title in response.css('div.post_con div.text.row div'):
            quote = title.css('div ::text').extract_first()
            quote = quote.replace('\n','').replace('\t','')
            decoded = html.unescape(quote)
            quote = unicodedata.normalize('NFD', decoded).encode('ascii', 'ignore').decode("utf-8")
            yield {'quote': quote}

        next_pages = response.css('div.pagination.row > a').extract()
        for index, page in enumerate(next_pages):
            if 'class="active"' in page:
                n_page = next_pages[index + 1]
                next_page = Selector(text=n_page).xpath('//a/@href').extract()
                next_page_url = next_page[0]
                if index == (len(next_pages) - 1):
                    next_page = False

        if next_page:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)
