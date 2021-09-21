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
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


def exec_scrapy(driver, url, d_aux):
    logging.info("Thread %s: starting", d_aux)
    path_novo = ("./4_bases_anuncios/")
    time.sleep(1)
    
    
    

    aux_carregou = 0
    while aux_carregou == 0:
        try:
            start = time.time()
            driver.get(get_scraperapi_url(url))
            end = time.time()
            tempo = str(round(end - start,0))
            aux_carregou += 1
        except:
            pass

    #id_anuncio = driver.find_element_by_xpath('/html/body/main/div/div[3]/div/div[2]/div[2]/div[5]/div[2]/form/input').get_attribute('value')
    #id_anuncio = driver.find_element_by_xpath('/html/body/main/div/div[1]/div/div/div[4]/div[3]/a').get_attribute('href').split('=')[1]
    try:
        aux1 = driver.find_element_by_xpath('/html/body/main/div/div/div/div/a[1]/span').text
        if aux1 == 'Sou novo':
            logging.info("Thread %s: finishing - SEM RESULTADO", d_aux)
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
                        titulo = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[1]/div/div[1]/div/div[1]/div/div[2]/h1').text
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


            try:    
                try:    
                    try:    
                        try:
                            marca = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[1]/th').text
                            #print('MARCA:', marca)
                            if marca == "Marca":    
                                marca1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[1]/td/span').text
                                #print('Marca:',marca1)
                            else:
                                marca1 = 'Não tem marca'
                        except:
                            marca = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[1]/th').text
                            if marca == 'Marca':
                                marca1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[1]/td/span').text
                                #print('Marca:',marca1)
                            else:
                                marca1 = 'Não tem marca'
                    except:
                        marca = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[1]/th').text
                        if marca == 'Marca':
                            marca1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[1]/td/span').text
                            #print('Marca:',marca1)
                        else:
                            marca1 = 'Não tem marca'
                except:
                    marca = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[1]/th').text
                    if marca == 'Marca':
                        marca1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[1]/td/span').text
                        #print('Marca:',marca1)
                    else:
                        marca1 = 'Não tem marca'
            except:
                marca1 = 'Não tem marca'
                #print(f'\033[31m'+str(marca1)+'\033[0;0m')

            try:    
                try:
                    linha = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[2]/th').text
                    #print('LINHA:',linha)
                    if linha == "Linha":
                        linha1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[2]/td/span').text
                        #print('Linha:',linha1)
                    else:
                        pass
                except:
                    linha = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[2]/th').text
                    #print('LINHA:',linha)
                    if linha == "Linha":
                        linha1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[2]/td/span').text
                        #print('Linha:',linha1)
                    else:
                        pass
            except:
                linha1 = 'Não tem linha'
                #print(f'\033[31m'+str(linha1)+'\033[0;0m')

            # try:
            #     try:
            #         try:
            #             try:
            #                 modelo = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[3]/th').text
            #                 #print('MODELO:',modelo)
            #                 if modelo == "Modelo":
            #                     modelo1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[3]/td/span').text
            #                     #print('Modelo:',modelo1)
            #                 else:
            #                     pass
            #             except:
            #                 modelo = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[2]/th').text
            #                 #print('MODELO:',modelo)
            #                 if modelo == "Modelo":
            #                     modelo1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[2]/td').text
            #                     #print('Modelo:', modelo1)
            #                 else:
            #                     pass
            #         except:
            #             modelo = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[2]/th').text
            #             if modelo == "Modelo":
            #                 modelo1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[2]/td/span').text
            #                 #print('Modelo', modelo1)
            #             else:
            #                 pass
            #     except:
            #         modelo = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[3]/th').text
            #         if modelo == "Modelo":
            #             modelo1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[3]/td/span').text
            #             #print('Modelo', modelo1)
            #         else:
            #             pass
            # except:
            #     modelo1 = 'Não tem modelo'
            #     #print(f'\033[31m'+str(modelo1)+'\033[0;0m')

            # try:
            #     try:
            #         try:
            #             try:
            #                 try:    
            #                     try:    
            #                         try:
            #                             numero_peca = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[4]/th').text
            #                             if numero_peca == 'Número de peça':
            #                                 numero_peca1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[4]/td/span').text
            #                                 #print('Numero de peça:', numero_peca1)
            #                             else:
            #                                 pass
            #                                 #print('Numero de peça: diferente')
            #                         except:
            #                             numero_peca = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[3]/th').text
            #                             if numero_peca == 'Número de peça':
            #                                 numero_peca1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[3]/td/span').text
            #                                 #print('Numero de peça:', numero_peca1)
            #                             else:
            #                                 pass
            #                     except:
            #                         numero_peca = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[2]/th').text
            #                         if numero_peca == 'Número de peça':
            #                             numero_peca1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[2]/td/span').text
            #                             #print('numero peça:',numero_peca1)
            #                         else:
            #                             pass
            #                 except:
            #                     numero_peca = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div/table/tbody/tr[2]/th').text
            #                     if numero_peca == 'Número de peça':
            #                         numero_peca1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div/table/tbody/tr[2]/td/span').text
            #                         #print('numero peça:',numero_peca1)
            #                     else:
            #                         pass
            #             except:
            #                 numero_peca = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[3]/th').text
            #                 if numero_peca == "Número de peça":
            #                     numero_peca1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[3]/td/span').text
            #                     #print('numero peça:', numero_peca1)
            #                 else:
            #                     pass
            #         except:
            #             numero_peca = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[4]/th').text
            #             if numero_peca == "Número de peça":
            #                 numero_peca1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[4]/td/span').text
            #                 #print('numero peça:', numero_peca1)
            #             else:
            #                 pass
            #     except:
            #         numero_peca = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[2]/th').text
            #         if numero_peca == "Número de peça":
            #             numero_peca1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[2]/td/span').text
            #             #print('numero peça:', numero_peca1)
            #         else:
            #             pass
            # except:
            #     numero_peca1 = 'Não tem numero da peça'
            #     #print(f'\033[31m'+str(numero_peca1)+'\033[0;0m')

            try:
                try:
                    try:    
                        try:    
                            try:
                                qntd_velas = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[5]/th').text
                                #print('Quantidade de velas:', qntd_velas)
                                if qntd_velas == 'Quantidade de velas':
                                    qntd_velas1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[5]/td/span').text
                                    #print('Quantidade de velas:',qntd_velas1)
                                else:
                                    pass
                            except:
                                qntd_velas = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[4]/th').text
                                if qntd_velas == 'Quantidade de velas':
                                    qntd_velas1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[4]/td/span').text
                                    #print('Quantidade de velas:', qntd_velas1)
                                else:
                                    pass
                        except:
                            qntd_velas = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[3]/th').text
                            if qntd_velas == 'Quantidade de velas':
                                qntd_velas1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[3]/td/span').text
                                #print('Quantidade de velas:',qntd_velas1)
                            else:
                                pass
                    except:
                        qntd_velas = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[4]/th').text
                        if qntd_velas == 'Quantidade de velas':
                            qntd_velas1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[4]/td/span').text
                            #print('Quantidade de velas:',qntd_velas1)
                        else:
                            pass
                except:
                    qntd_velas = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[5]/th').text
                    if qntd_velas == 'Quantidade de velas':
                        qntd_velas1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[5]/td/span').text
                        #print('Quantidade de velas:',qntd_velas1)
                    else:
                        pass
            except:
                qntd_velas1 = 'Não tem quantidade de velas'
                #print(f'\033[31m'+str(qntd_velas1)+'\033[0;0m')

            dicionario = {"titulo":titulo,
                    "preco":preco.replace('\n', ''),
                    "condicao":condicao,
                    "qtd_vendida":vendas,
                    "marca":marca1,
                    # "linha": linha1,
                    # "modelo": modelo1,
                    # "numero_peca":numero_peca1,
                    # "qntd_velas":qntd_velas1,
                    "url": url,
                    "id_anuncio": id_anuncio
            }

            with open(path_novo + "{}.txt".format(str(time.time()).replace('.', '')), 'w', encoding = 'utf-8') as f:
                f.write(json.dumps(dicionario))

            del titulo, preco, condicao, vendas, marca1, url

            logging.info("Thread %s: finishing", d_aux)
            return 'OK'
    except:
        logging.info("Thread %s: finishing - ERRO NO AUX1", d_aux)
        return 'FAZER'


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
        retorno_funcao = exec_scrapy(driver, row['url'], sys.argv[2])
        rows.loc[index, 'status'] = retorno_funcao
        rows.to_csv(path + sys.argv[1])

    driver.quit()

"""
taskkill /F /IM firefox.exe /T
taskkill /F /IM geckodriver.exe /T
"""