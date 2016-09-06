# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.utils.response import open_in_browser, body_or_str
from re import search, sub
from feeder.utils import html2text
from feeder.items import Article
import arrow


class DeloSpider(scrapy.Spider):
    name = "delo"
    allowed_domains = ["m.delo.si"]
    base_url = 'http://m.delo.si'

    def start_requests(self):
        return (Request(self.base_url + '/%s/page/%d' % (category, page), headers={'Referer': self.base_url}) for
                (category, page) in
                ((category, page) for category in self.categories for page in range(1, self.number_of_pages)))

    @property
    def number_of_pages(self):
        return 100

    @property
    def categories(self):
        return ['novice', 'gospodarstvo']  # + svet

    def parse(self, response):
        if search('/page/\d+$', response.url):
            return self.parse_index(response)
        else:
            article = self.parse_article(response)
            return article

    def parse_index(self, response):
        return (Request(self.base_url + path, headers={'Referer': response.url}) for path in
                response.css('.article_box a').xpath('@href').extract())

    def parse_article(self, response):
        title = ''.join(response.css('title::text').extract())
        article = sub('\s\s+', ' ', ''.join(response.css('div.article').xpath('./node()').extract()))

        return Article(
            domain='delo.si',
            scraped_at=arrow.utcnow(),
            scraped_url=response.url,
            mobile_source_url=response.url,
            desktop_source_url=sub('m\.delo', 'www.delo', response.url, 1),
            title_raw=title,
            body_raw=article,
            image_urls=self.parse_images(response),
            date_at_raw=self.parse_date(response)
        )

    def parse_images(self, response):
        return [self.base_url + img for img in response.css('div.article img').xpath('@src').extract()]

    def parse_date(self, response):
        image_urls = [img for img in self.parse_images(response) if search('\d{8}', img) is not None]

        if len(image_urls) == 0:
            return None

        image_url = image_urls[0]
        url_datetime = search('(\d{8})', image_url)
        if not url_datetime:
            return None

        time_raw = ('' + response.css('div.article .small_text::text').extract()[1]).lstrip().rstrip()
        match_time_raw = search('(\d{2}:\d{2})', time_raw)
        if not match_time_raw:
            return None

        date = arrow.get(url_datetime.group(0) + '-' + match_time_raw.group(0),
                         ['YYYYMMDD-HH:mm', 'YYYYMMDD']) \
            .replace(tzinfo='Europe/Ljubljana') \
            .to('UTC')

        return date
