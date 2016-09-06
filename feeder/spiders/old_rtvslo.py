# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from datetime import datetime, timedelta
from re import sub, match, search

# TODO: This was improted from one older project. Needs to be rewritten!

class RtvsloSpider(scrapy.Spider):
    name = "rtvslo"
    allowed_domains = ["rtvslo.si"]
    # categories = ["slovenija", "gospodarstvo", "lokalne-novice", "crna-kronika"]
    categories = ["slovenija"]

    def start_requests(self):
        date_from = self.date_from
        if self.mode == 'archive':
            date_from = (datetime.now() - timedelta(days=356)).strftime("%Y-%m-%d")

        return (Request("http://www.rtvslo.si/%s/arhiv/?%s" % (x, urlencode({
            'date_to': self.date_to,
            'date_from': date_from,
            'page': 0,
        })), callback=self.parse_archive_page) for x in self.categories)

    # Parses one page of archive:
    # Example: http://www.rtvslo.si/slovenija/arhiv/?date_from=2015-01-15&page=110&date_to=2016-01-06
    def parse_archive_page(self, response):
        titles = [x.extract() for x in
                  response.xpath("//div[@class='contents'][2]//div[@id='sectionlist']//a/text()")]

        excerpts = [x.extract() for x in
                    response.xpath("//div[@class='contents'][2]//div[@id='sectionlist']//span[@class='text']/text()")]

        original_urls = ["http://www.rtvslo.si%s" % x.extract() for x in
                         response.xpath("//div[@class='contents'][2]//div[@id='sectionlist']//a[@class='title']/@href")]

        ids = [match(".*\/(\d+)", x).group(1) for x in original_urls]

        urls = ["http://www.rtvslo.si/index.php?c_mod=news&op=print&id=%s" % id for id in ids]

        requests = [
            Request(item[0],
                    callback=self.parse_article_print,
                    meta={
                        'article': {'extract_url': item[0], 'aid': ("rtvslo-%s" % item[1]), 'title': item[2],
                                    'excerpt': item[3],
                                    'url': item[4], 'site': 'rtvslo'}}) for item in
            zip(urls, ids, titles, excerpts, original_urls)]

        # Check for next page
        next_item = response.xpath("//div[@class='rpagin']//a[@class='next']")
        if len(next_item) != 0:
            page = int(match(".*page=(\d+)", response.url).group(1), base=10)
            new_page = page + 1
            requests.append(Request(replace(response.url, "page=%d" % page, "page=%d" % new_page),
                                    callback=self.parse_archive_page))

        return requests

    # Parses "print" page of article to get "clean" content.
    # Example: http://www.rtvslo.si/index.php?c_mod=news&op=print&id=355858
    def parse_article_print(self, response):
        article = Article(**response.meta['article'])
        article['content'] = "\n".join(
            response.xpath("//div[@id='newsbody']/*[not(contains(@id,'newsblocks'))]").extract())
        return article

    def parse(self, response):
        pass
