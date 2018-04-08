# -*- coding: utf-8 -*-
import scrapy
from string import Template


class IqiyiSpider(scrapy.Spider):
    category = 'anime'
    name = category + '.' + 'iqiyi'
    protocol = 'http'
    allowed_domains = ['list.tw.iqiyi.com']
    url = Template('http://list.tw.iqiyi.com/www/4/-------------11-${page}-1-iqiyi--.html')
    page = 1
    start_urls = [url.substitute(page=page)]

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

        self.page = self.page + 1
        next_page = self.url.substitute(page=self.page)
        yield response.follow(next_page, self.parse)
