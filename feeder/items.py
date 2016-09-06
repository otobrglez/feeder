# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Article(scrapy.Item):
    domain = scrapy.Field()
    scraped_at = scrapy.Field()
    scraped_url = scrapy.Field()
    mobile_source_url = scrapy.Field()
    desktop_source_url = scrapy.Field()
    title_raw = scrapy.Field()
    body_raw = scrapy.Field()
    date_at_raw = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
