import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import re

cidade = input('Digite a cidade que voce deseja pesquisar: ')

options = Options()

options.add_argument('window-size=900,800')

navegador = webdriver.Chrome(options=options)

navegador.get('https://www.airbnb.com.br/')

sleep(3)

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

hospedagens = site.findAll('div', attrs={'itemprop':'itemListElement'}) # Procura pelos itens
for hospedagem in hospedagens:
  hospedagem_nome = hospedagem.find('div', attrs={'data-testid':'listing-card-title'})              # Captura o nome
  hospedagem_detalhes = hospedagem.findAll('div', attrs={'data-testid':'listing-card-subtitle'})    # Captura os detalhes
  hospedagem_url = hospedagem.find('meta', attrs={'itemprop': 'url'})                               # Captura a url
  hospedagem_preco = hospedagem.find('span', attrs={'class':'a8jt5op'})                             # Captura o preço
  valor_por_noite = hospedagem_preco.text

  valor_numérico = re.search(r'\d+', valor_por_noite).group()                                       # Filtra o preço
  hospedagem_detalhes = ''.join([detalhe.text + ', ' for detalhe in hospedagem_detalhes])           # Faz um join de todos detalhes

  print('Nome:', hospedagem_nome.text)
  print('Detalhes:', hospedagem_detalhes)
  print('URL:', hospedagem_url['content'])
  print('Valor por noite: R$', valor_numérico)
  print()