Ferramenta desenvolvida com o framework [Scrapy](https://scrapy.org), usada para raspar informações sobre os serviços disponíveis no Portal RJ Digital

# Como usar
Os comandos abaixo preparam o ambiente em sistema operacional Windows. É necessário ter o [Python](https://docs.python.org/3/) (+3.0) instalado.

## Criar ambiente virtual
``` console
python -m venv .venv
```

## Ativar ambiente virtual
``` console
.\.venv\Scripts\Activate.ps1
```

## Instalar dependências
``` console
pip install -r .\requirements.txt
```

## Executar raspador
``` console
scrapy crawl rj_digital_servicos
```

Ao final da execução, os 2 arquivos na pasta json são atualizados: 
- ***servicos.json*** - Que contém as informações sobre todos os serviços dispníveis no Portal
- ***sites_externos.json*** - Arquivo auxiliar com o retorno da requisição para o site cadastrado no campo URL_EXTERNO de cada serviço disponível no Portal.
