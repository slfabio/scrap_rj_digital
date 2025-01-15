# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class SiteExterno(scrapy.Item):
    data_acesso = scrapy.Field()
    url_resposta = scrapy.Field()
    id = scrapy.Field()
    titulo = scrapy.Field()
    orgao_sigla = scrapy.Field()
    url = scrapy.Field()
    url_externo = scrapy.Field()