# -*- coding: utf-8 -*-
import scrapy
from string import Template

url = Template('http://list.tw.iqiyi.com/www/4/-------------11-${page}-1-iqiyi--.html')

class IqiyiSpider(scrapy.Spider):
    category = 'anime'
    name = category + '.' + 'iqiyi'
    protocol = 'http'
    allowed_domains = ['list.tw.iqiyi.com']
    start_urls = map(lambda p: url.substitute(page=p), range(1, 20))

    def parse(self, response):
        items = response.css('div.plist-item')
        if not items:
            return

        for anime in items:
            title = anime.css('p.pic-sub-title::text').extract_first()
            if not title:
                continue

            href = anime.css('a.tw-list-link::attr(href)').extract_first()
            i = href.find('com/')
            key = href[(i+4):-5]

            image = anime.css('a.tw-list-link::attr(v-i71-anim-img)').extract_first()
            image = image[1:-1]

            yield {
                'id': self.name + '::' + key,
                'title': anime.css('p.pic-sub-title::text').extract_first(),
                'link': self.protocol + ':' + href,
                'image': self.protocol + ':' + image,
                'info': anime.css('p.pic-inner-title::text').extract_first()
            }
