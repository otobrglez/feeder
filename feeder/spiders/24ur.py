from feeder.spiders import FeederSpider
from urllib.parse import urlencode

from scrapy import Request
from scrapy.utils.response import open_in_browser, body_or_str
from re import search, sub
from feeder.utils import html2text
from feeder.items import Article
import arrow
from re import sub
from json import loads, load
from pprint import pprint
from pdb import set_trace


class Ur24(FeederSpider):
    name = "24ur"
    base_url = 'http://m.24ur.com'
    api_url = 'http://api.24ur.si'
    allowed_domains = ['http://m.24ur.com', 'http://api.24ur.si']
    mode = 'refresh'
    over_pages = None
    over_categories = None

    def start_requests(self):
        return (
            Request(self.api_url + '/spored/oldFront/get/%s?%s' % (category, urlencode({'external': 1, 'page': page})),
                    headers={'Referer': self.base_url})
            for
            (category, page) in
            ((category, page) for category in self.categories for page in range(1, self.number_of_pages)))

    @property
    def categories(self):
        cats = []
        if self.over_categories:
            cats = self.over_categories
        else:
            cats = ['novice/slovenija']

        return [sub('/', '%2F', "/%s/" % c) for c in cats]

    @property
    def number_of_pages(self):
        if self.over_pages:
            return self.over_pages

        if self.mode == 'refresh':
            return 5
        elif self.mode == 'big':
            return 200
        else:
            raise Exception('Unknown mode')

    def parse(self, response):
        return self.parse_index(response)

    def parse_index(self, response):
        data = loads(response.body_as_unicode())
        articles = [self.raw_to_article(a, response) for a in data['content']]
        return articles

    def raw_to_article(self, data, response):
        return Article(
            domain='24ur.com',
            scraped_at=arrow.utcnow(),
            scraped_url=self.base_url + data['url'],
            mobile_source_url=self.base_url + data['url'],
            desktop_source_url=sub('m\.24ur', 'www.24ur', (self.base_url + data['url']), 1),
            title_raw=data['title'],
            title_clean=data['title'],
            body_raw=data['body'],
            image_urls=self.parse_images(data['images']),
            date_at=self.parse_date(data['date'])
        )

    def parse_date(self, stamp):
        return arrow.get(stamp)

    def parse_images(self, images):
        return [sub('PLACEHOLDER', '800x575', x['href']) for x in images]
