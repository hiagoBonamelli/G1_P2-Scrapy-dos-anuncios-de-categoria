from selenium.webdriver.firefox.options import Options

from selenium import webdriver

import multiprocessing.pool as mpool
import concurrent.futures
import pandas as pd
import numpy as np
import threading
import logging
import sqlite3
import random
import time
import json
import sys
import os

from urllib.parse import urlencode
from bs4 import BeautifulSoup
import requests


API_KEY = "a1f5eae4966a5e0e09ec7d83b2f3819e"


def get_scraperapi_url(url):
    """
        Converts url into API request for ScraperAPI.
    """
    #payload = {'api_key': API_KEY, 'url': url}
    #proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    proxy_url = url
    return proxy_url


def exec_scrapy(driver, url, d_aux, id_anuncio):
    logging.info("Thread %s: starting", d_aux)
    path_novo = ("./4_bases_anuncios/")
    time.sleep(5)
    
    
    

    aux_carregou = 0
    while aux_carregou == 0:
        try:
            start = time.time()
            driver.get(get_scraperapi_url(url))
            end = time.time()
            tempo = str(round(end - start,0))
            aux_carregou += 1
            try:
                driver.find_element_by_class_name('ui-search-results')
                aux1 = 'Sou novo'
            except:
                aux1 = driver.find_element_by_xpath('/html/body/main/div/div/div/div/a[1]/span').text
        except:
            aux1 = driver.find_element_by_xpath("/html/body").text

    #id_anuncio = driver.find_element_by_xpath('/html/body/main/div/div[3]/div/div[2]/div[2]/div[5]/div[2]/form/input').get_attribute('value')
    #id_anuncio = driver.find_element_by_xpath('/html/body/main/div/div[1]/div/div/div[4]/div[3]/a').get_attribute('href').split('=')[1]
    #try:
    #try:
        #driver.find_element_by_class_name('ui-search-results')
        #aux1 = 'Sou novo'
    #except:
        #aux1 = driver.find_element_by_xpath('/html/body/main/div/div/div/div/a[1]/span').text

    if aux1 == 'Sou novo':
        logging.info("Thread %s: finishing - SEM RESULTADO", d_aux)
        with open("./4_excluir/{}.txt".format(id_anuncio), 'w', encoding = 'utf-8') as f:
            os.utime(path, None)
        return 'FAZER'
    elif aux1 == 'Timed out waiting for response from target.':
        logging.info("Thread %s: finishing - Timed out waiting for response from target.", d_aux)
        return 'FAZER'
    else:
        try:
            id_anuncio = driver.find_element_by_xpath('/html/body/main/div/div[4]/div[1]/div/p/span').text.replace('#', '')
        except:
            id_anuncio = driver.find_element_by_xpath('/html/body/main/div/div[5]/div[1]/div/p/span').text.replace('#', '')
        logging.info("id anuncio %s", id_anuncio)

        try:
            try:
                try:
                    try:
                        titulo = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[1]/div/div[1]/div/div[1]/div/div[2]/h1').text
                    except:
                        titulo = driver.find_element_by_xpath('/html/body/main/div/div[3]/div/div[1]/div[1]/div/div[1]/div/div/h1').text
                except:
                    titulo = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[1]/div[1]/div/div[1]/div/div[2]/h1').text
            except:
                titulo = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[1]/div[1]/div/div[1]/div/div[2]/h1').text
        except:
            try:
                titulo = driver.find_element_by_xpath('/html/body/main/div/div[4]/div/div[1]/div/div[1]/div/div[1]/div/div[2]/h1').text
            except:
                titulo = driver.find_element_by_xpath('/html/body/main/div/div[3]/div/div[1]/div/div[1]/div/div[1]/div/div/h1').text


        try:
            try:
                try:
                    preco = driver.find_element_by_xpath('/html/body/main/div/div[3]/div/div[1]/div/div[1]/div/div[2]/div/div[1]/span/span[2]').text
                    preco = preco.replace('\n', '')
                except:
                    preco = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[1]/div/div[1]/div/div[2]/div/div[1]/span/span[2]').text
                    preco = preco.replace('\n', '')
            except:
                preco = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[1]/div[1]/div/div[2]/div/div[1]/span/span[2]').text
                preco = preco.replace('\n', '')
        except:
            try:
                preco = driver.find_element_by_xpath('/html/body/main/div/div[4]/div/div[1]/div/div[1]/div/div[2]/div/div[1]/span/span[2]').text
                preco = preco.replace('\n', '')
            except:
                preco = driver.find_element_by_xpath('/html/body/main/div/div[3]/div/div[1]/div/div[1]/div/div[3]/div/div[1]/span/span[2]').text
                preco = preco.replace('\n', '')
                

        try:
            vendas_condicao = driver.find_element_by_xpath("/html/body/main/div/div[3]/div/div[1]/div/div[1]/div/div[1]/div/div[1]").text
            if vendas_condicao == 'Ver os meios de pagamento':
                raise Exception('I know Python!')
            else:
                condicao = vendas_condicao.split("|")[0].strip()
                try:
                    vendas = int(vendas_condicao.split("|")[1].split()[0])
                except:
                    vendas = 0
        except:
            try:
                vendas_condicao = driver.find_element_by_xpath("/html/body/main/div/div[3]/div/div[1]/div[1]/div/div[1]/div/div[1]").text
                condicao = vendas_condicao.split("|")[0].strip()
                try:
                    vendas = int(vendas_condicao.split("|")[1].split()[0])
                except:
                    vendas = 0

            except:
                vendas_condicao = driver.find_element_by_xpath('/html/body/main/div/div[4]/div/div[1]/div/div[1]/div/div[1]/div/div[1]').text
                condicao = vendas_condicao.split("|")[0].strip()
                try:
                    vendas = int(vendas_condicao.split("|")[1].split()[0])
                except:
                    vendas = 0

        # verificar se existe tabela de caracteristicas
        try:
            driver.find_elements_by_class_name('andes-table')

            try:
                tabela_caracteristicas = driver.find_element_by_xpath('/html/body/main/div/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody')
            except:
                tabela_caracteristicas = driver.find_element_by_xpath('/html/body/main/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody')

            linhas_tabela = tabela_caracteristicas.find_elements_by_tag_name('tr')
            dict_caracteristicas = {}
            for l in linhas_tabela:
                chave = l.find_element_by_tag_name('th').text
                valor = l.find_element_by_tag_name('td').text
                dict_caracteristicas[chave] = valor

            if "Marca" in dict_caracteristicas:
                marca1 = dict_caracteristicas['Marca']
            else:
                marca1 = 'Não tem'

            if "Modelo" in dict_caracteristicas:
                modelo1 = dict_caracteristicas['Modelo']
            else:
                modelo1 = 'Não tem'

            if "Número de peça" in dict_caracteristicas:
                numero_peca1 = dict_caracteristicas['Número de peça']
            else:
                numero_peca1 = 'Não tem'
        
        except:
            marca1 = 'Não tem'
            modelo1 = 'Não tem'
            numero_peca1 = 'Não tem'

        dicionario = {"titulo":titulo,
                "preco":preco.replace('\n', ''),
                "condicao":condicao,
                "qtd_vendida":vendas,
                "marca":marca1,
                "modelo": modelo1,
                "numero_peca":numero_peca1,
                "url": url,
                "id_anuncio": id_anuncio
        }

        with open(path_novo + "{}.txt".format(str(time.time()).replace('.', '')), 'w', encoding = 'utf-8') as f:
            f.write(json.dumps(dicionario))

        del titulo, preco, condicao, vendas, marca1, url

        logging.info("Thread %s: finishing", d_aux)
        return 'OK'
    #except:
        #logging.info("Thread %s: finishing - ERRO NO AUX1", d_aux)
        #return 'FAZER'


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    options = Options()
    options.headless = False
    driver = webdriver.Firefox(options=options)

    # path
    path = './4_lista_df/'

    # ler csv
    rows = pd.read_csv(path + sys.argv[1], index_col=0)
    rows = rows[rows['status'] == 'FAZER']

    for index, row in rows.iterrows():
        logging.info("Row %s", list(row))
        retorno_funcao = exec_scrapy(driver, row['url'], sys.argv[2], row['id_anuncio'])
        rows.loc[index, 'status'] = retorno_funcao
        rows.to_csv(path + sys.argv[1])

    driver.quit()

"""
taskkill /F /IM firefox.exe /T
taskkill /F /IM geckodriver.exe /T
"""