# -*- coding: utf-8 -*-
import scrapy


class GamerSpider(scrapy.Spider):
    category = 'anime'
    name = category + '.' + 'gamer'
    baseUrl = 'https://ani.gamer.com.tw'
    allowed_domains = ['ani.gamer.com.tw']
    start_urls = [baseUrl + '/animeList.php']

    def parse(self, response):
        for anime in response.css('ul.anime_list > li'):
            title = anime.css('div.info > b::text').extract_first()
            if not title:
                continue

            href = anime.css('a::attr(href)').extract_first()
            i = href.find('sn=')
            sn = href[(i+3):]
            yield {
                'id': self.name + '::' + sn,
                'title': title,
                'link': self.baseUrl + href,
                'image': anime.css('div.pic::attr(data-bg)').extract_first(),
                'info': anime.css('div.info::text').extract_first()
            }

        for next_page in response.css('div.page_number > a::attr(href)'):
            yield response.follow(next_page, self.parse)
