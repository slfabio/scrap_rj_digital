# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

class RjDigitalPipeline:
    def open_spider(self, spider):
        # Abrir dois arquivos separados para gravar os dados
        self.arq_servico = open('./json/servicos.json', 'w', encoding='utf-8')
        self.arq_servico.write('[\n')
        self.arq_url_externa = open('./json/sites_externos.json', 'w', encoding='utf-8')
        self.arq_url_externa.write('[\n')

    def close_spider(self, spider):
        # Fechar os arquivos quando o spider terminar
        self.arq_servico.seek(self.arq_servico.tell()-4) # remove a ultima linha para remover a virgula
        self.arq_servico.truncate()
        self.arq_servico.write('}\n]')
        self.arq_servico.close()

        self.arq_url_externa.seek(self.arq_url_externa.tell()-4) # remove a ultima linha para remover a virgula
        self.arq_url_externa.truncate()
        self.arq_url_externa.write('}\n]')
        self.arq_url_externa.close()

    def process_item(self, item, spider):
        if "url_resposta" in item.keys():
            item["data_acesso"] = str(item["data_acesso"])
            json.dump(item, self.arq_url_externa, ensure_ascii=False, indent=4)
            self.arq_url_externa.write(',\n')
        else:
            json.dump(item, self.arq_servico, ensure_ascii=False, indent=4)
            self.arq_servico.write(',\n')
        return item