import requests
import os
import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import re

cidade = input('Digite a cidade que voce deseja pesquisar: ')

options = Options()

options.add_argument('window-size=900,800')

navegador = webdriver.Chrome(options=options)

navegador.get('https://www.airbnb.com.br/')

sleep(4)

input_place2 = navegador.find_element(By.CLASS_NAME, "_160gnkxa") # Aceita o cookie
input_place2.click()

sleep(3)

input_place3 = navegador.find_element(By.CLASS_NAME, "f19g2zq0")  # Clica em 'Qualquer lugar'
input_place3.click()

sleep(3)

input_place = navegador.find_element(By.CLASS_NAME, "iluujbk")    # Procura o input
input_place.send_keys(cidade)                                     # Insere a cidade e pesquisa
input_place.submit()

sleep(3)

page_content = navegador.page_source

site = BeautifulSoup(page_content, 'html.parser')                   # Pega o conteúdo html
dados_hospedagens = []

hospedagens = site.findAll('div', attrs={'itemprop':'itemListElement'}) # Procura pelos itens
for hospedagem in hospedagens:
  hospedagem_nome = hospedagem.find('div', attrs={'data-testid':'listing-card-title'})              # Captura o nome
  hospedagem_detalhes = hospedagem.findAll('div', attrs={'data-testid':'listing-card-subtitle'})    # Captura os detalhes
  hospedagem_url = hospedagem.find('meta', attrs={'itemprop': 'url'})                               # Captura a url
  hospedagem_preco = hospedagem.find('div', attrs={'class':'_1jo4hgw'}).text                        # Captura o preco
  hospedagem_detalhes = ''.join([detalhe.text + ', ' for detalhe in hospedagem_detalhes])           # Faz um join de todos detalhes
  dados_hospedagens.append([hospedagem_nome.text, hospedagem_detalhes, hospedagem_url['content'], hospedagem_preco])

dados = pd.DataFrame(dados_hospedagens, columns=['Nome', 'Detalhes', 'URL', 'Valor'])
data = datetime.datetime.now()
dia = data.day
mes = data.month
ano = data.year

cidade = cidade.replace(' ', '_')
caminho = os.path.join('dados-cidades', cidade)
nome_arquivo = f'({dia}-{mes}-{ano}).csv'

if not os.path.exists(caminho):
    os.makedirs(caminho)

dados.to_csv(os.path.join(caminho, nome_arquivo), index=False)