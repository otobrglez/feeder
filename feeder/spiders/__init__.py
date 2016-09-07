# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy


class FeederSpider(scrapy.Spider):
    mode = 'refresh'
    over_pages = None
    over_categories = None

    def __init__(self, mode='refresh', pages=None, categories=None, *args, **kwargs):
        super(FeederSpider, self).__init__(*args, **kwargs)
        self.mode = mode

        if pages is not None:
            self.over_pages = int('' + pages)

        if categories is not None:
            self.over_categories = ('' + categories).split(',')
