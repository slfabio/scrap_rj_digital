import scrapy
import w3lib

class PlaywrightSpider(scrapy.Spider):

    def parse(self, response):
        from scrapy.http.response.html import HtmlResponse
        ht = HtmlResponse(url=response.url, body=response.body, encoding="utf-8", request=response.request)
        return None
