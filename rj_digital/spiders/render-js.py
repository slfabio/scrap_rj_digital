import scrapy
import w3lib

class PlaywrightSpider(scrapy.Spider):
    name = "playwright"
    start_urls = ["https://resultados.tse.jus.br/oficial/app/index.html#/eleicao;e=e619;uf=rj;mu=58653;tipo=3/resultados/cargo/13"]  # avoid using the default Scrapy downloader

    def parse(self, response):
        from scrapy.http.response.html import HtmlResponse
        ht = HtmlResponse(url=response.url, body=response.body, encoding="utf-8", request=response.request)
        return None