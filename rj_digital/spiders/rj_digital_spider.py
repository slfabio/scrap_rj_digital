import re
import html
from bs4 import BeautifulSoup

import scrapy
from datetime import datetime

class RjSpider(scrapy.Spider):
    name = "rj_digital_servicos"
    RJ_DIGITAL_HEADERS = {
        'Accept': 'application/json, text/plain, */*',
        'Authorization': 'Api-Key WAwXKO97.XAqEhNSo5khRfEuzAWyqMiC89Jaf1YeW',
    }
    slug_servicos = []

    def start_requests(self):
        perfis = ['Cidad%C3%A3o', 'Empresa', 'Gest%C3%A3o%20P%C3%BAblica', 'Servidor']
        for perfil in perfis:
            yield scrapy.Request(
                        url = f'https://admin.rj.gov.br/api/cms/categorias/?perfil={perfil}',
                        headers=self.RJ_DIGITAL_HEADERS,
                        callback = self.request_sub_categoria
                    )

    def request_sub_categoria(self, response):
        for categoria in response.json():
            for sub_categoria in categoria['subtopicos']:
                slug = sub_categoria['slug']
                yield scrapy.Request(
                    url = f'https://admin.rj.gov.br/api/cms/servicos_busca/?subcategoria_slug={slug}',
                    headers=self.RJ_DIGITAL_HEADERS,
                    callback = self.request_servico
                )
    
    def request_servico(self, response):
        for servico in response.json():
            if servico['slug'] not in self.slug_servicos:
                self.slug_servicos.append(servico['slug'])
                slug = servico['slug']
                yield scrapy.Request(
                    url = f'https://admin.rj.gov.br/api/cms/servicos_busca/?slug={slug}',
                    headers=self.RJ_DIGITAL_HEADERS,
                    callback = self.parse_servico
                )

    def parse_servico(self, response):
        servico = response.json()[0]
        servico['url'] = f"https://www.rj.gov.br/servico/{servico['slug']}"
        servico = self.decode_html(servico)
        yield servico

        url_ext = servico['url_externo']
        if url_ext and not url_ext.startswith("https://portal.idp.rj.gov.br"):
            yield scrapy.Request(
                url = url_ext,
                callback = self.parse_url_externa,
                cb_kwargs={"servico": servico},
                #headers={},
                dont_filter = True 
            )


    def parse_url_externa(self, response, servico):
        yield {
            "data_acesso": datetime.now(),
            "id": servico['id'],
            "titulo": servico['titulo'],
            "orgao_sigla": servico['orgao_sigla'],
            "url": servico['url'],
            "url_externo": servico['url_externo'],
            "url_resposta": response.url,
        }

    
    def decode_html(self, servico):
        for campo in servico.keys():
            valor_campo = servico.get(campo, None)
            txt_decod =  self.texto_decodificado(campo, valor_campo)
            if txt_decod:
                servico[campo] = txt_decod
            if isinstance(valor_campo, list):
                for item in valor_campo:
                    if isinstance(item, dict):
                        for key, value in item.items():
                            txt_decod =  self.texto_decodificado(campo, value)
                            if txt_decod:
                                item[key] = txt_decod
        return servico

    def texto_decodificado(self, campo, valor_campo):
        if isinstance(valor_campo, str) and not campo.startswith('url'):
            texto = re.sub(r'<a\s+[^>]*>|<\/a>', '', valor_campo) #remove tags de link
            texto = BeautifulSoup(texto, "lxml").text #faz o parse das tags html
            texto = html.unescape(texto) # substitui codigos html por texto
            return texto
        return None
