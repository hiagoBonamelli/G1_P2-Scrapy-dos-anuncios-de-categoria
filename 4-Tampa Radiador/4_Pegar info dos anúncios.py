from selenium.webdriver.firefox.options import Options
from urllib.parse import urlencode
from selenium import webdriver

import multiprocessing.pool as mpool
import concurrent.futures
import pandas as pd
import threading
import logging
import sqlite3
import random
import time
import json
import os


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
    path_novo = ("C:/Users/Hiago Bonomelli/Documents/aux_infos/")
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
    

    try:
        try:
            try:
                titulo = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[1]/div/div[1]/div/div[1]/div/div[2]/h1').text
                #print('Titulo:',titulo)
            except:
                titulo = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[1]/div[1]/div/div[1]/div/div[2]/h1').text
                #print('Titulo:',titulo)
        except:
            titulo = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[1]/div[1]/div/div[1]/div/div[2]/h1').text
            #print('Titulo:',titulo)
    except:
        titulo = 'Não tem titulo'
        #print(f'\033[31m'+str(titulo)+'\033[0;0m')

    try:
        try:
            try:
                preco = driver.find_element_by_xpath('/html/body/main/div/div[3]/div/div[1]/div/div[1]/div/div[2]/div/div[1]/span/span[2]').text
                preco.replace('\n', '')
            except:
                preco = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[1]/div/div[1]/div/div[2]/div/div[1]/span/span[2]').text
                preco.replace('\n', '')
        except:
            preco = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[1]/div[1]/div/div[2]/div/div[1]/span/span[2]').text
            preco.replace('\n', '')
    except:
        preco = 'não tem preço'
        #print(f'\033[31m'+str(preco)+'\033[0;0m')


    try:
        vendas_condicao = driver.find_element_by_xpath("/html/body/main/div/div[3]/div/div[1]/div/div[1]/div/div[1]/div/div[1]/span").text
        try:
            condicao = vendas_condicao.split("|")[0].strip()
        except:
            condicao = 'Nao tem condicao'
        try:
            vendas = int(vendas_condicao.split("|")[1].split()[0])
        except:
            vendas = 0
    except:
        try:
            vendas_condicao = driver.find_element_by_xpath("/html/body/main/div/div[3]/div/div[1]/div[1]/div/div[1]/div/div[1]/span").text
            try:
                condicao = vendas_condicao.split("|")[0].strip()
            except:
                condicao = 'Nao tem condicao'
            try:
                vendas = int(vendas_condicao.split("|")[1].split()[0])
            except:
                vendas = 0

        except:
            vendas = 'Não tem qntd de vendas'
            condicao = 'Nao tem condicao'


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
                        sys.exit()
                except:
                    marca = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[1]/th').text
                    if marca == 'Marca':
                        marca1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[1]/td/span').text
                        #print('Marca:',marca1)
                    else:
                        sys.exit()
            except:
                marca = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[1]/th').text
                if marca == 'Marca':
                    marca1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[1]/td/span').text
                    #print('Marca:',marca1)
                else:
                    sys.exit()
        except:
            marca = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[1]/th').text
            if marca == 'Marca':
                marca1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[1]/td/span').text
                #print('Marca:',marca1)
            else:
                sys.exit()
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
                sys.exit()
        except:
            linha = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[2]/th').text
            #print('LINHA:',linha)
            if linha == "Linha":
                linha1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[2]/td/span').text
                #print('Linha:',linha1)
            else:
                sys.exit()
    except:
        linha1 = 'Não tem linha'
        #print(f'\033[31m'+str(linha1)+'\033[0;0m')

    try:
        try:
            try:
                try:
                    modelo = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[3]/th').text
                    #print('MODELO:',modelo)
                    if modelo == "Modelo":
                        modelo1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[3]/td/span').text
                        #print('Modelo:',modelo1)
                    else:
                        sys.exit()
                except:
                    modelo = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[2]/th').text
                    #print('MODELO:',modelo)
                    if modelo == "Modelo":
                        modelo1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[2]/td').text
                        #print('Modelo:', modelo1)
                    else:
                        sys.exit()
            except:
                modelo = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[2]/th').text
                if modelo == "Modelo":
                    modelo1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[2]/td/span').text
                    #print('Modelo', modelo1)
                else:
                    sys.exit()
        except:
            modelo = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[3]/th').text
            if modelo == "Modelo":
                modelo1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[3]/td/span').text
                #print('Modelo', modelo1)
            else:
                sys.exit()
    except:
        modelo1 = 'Não tem modelo'
        #print(f'\033[31m'+str(modelo1)+'\033[0;0m')

    try:
        try:
            try:
                try:
                    try:    
                        try:    
                            try:
                                numero_peca = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[4]/th').text
                                if numero_peca == 'Número de peça':
                                    numero_peca1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[4]/td/span').text
                                    #print('Numero de peça:', numero_peca1)
                                else:
                                    sys.exit()
                                    #print('Numero de peça: diferente')
                            except:
                                numero_peca = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[3]/th').text
                                if numero_peca == 'Número de peça':
                                    numero_peca1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[3]/td/span').text
                                    #print('Numero de peça:', numero_peca1)
                                else:
                                    sys.exit()
                        except:
                            numero_peca = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[2]/th').text
                            if numero_peca == 'Número de peça':
                                numero_peca1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[2]/td/span').text
                                #print('numero peça:',numero_peca1)
                            else:
                                sys.exit()
                    except:
                        numero_peca = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div/table/tbody/tr[2]/th').text
                        if numero_peca == 'Número de peça':
                            numero_peca1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div/table/tbody/tr[2]/td/span').text
                            #print('numero peça:',numero_peca1)
                        else:
                            sys.exit()
                except:
                    numero_peca = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[3]/th').text
                    if numero_peca == "Número de peça":
                        numero_peca1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[3]/td/span').text
                        #print('numero peça:', numero_peca1)
                    else:
                        sys.exit()
            except:
                numero_peca = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[4]/th').text
                if numero_peca == "Número de peça":
                    numero_peca1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[4]/td/span').text
                    #print('numero peça:', numero_peca1)
                else:
                    sys.exit()
        except:
            numero_peca = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[2]/th').text
            if numero_peca == "Número de peça":
                numero_peca1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[2]/td/span').text
                #print('numero peça:', numero_peca1)
            else:
                sys.exit()
    except:
        numero_peca1 = 'Não tem numero da peça'
        #print(f'\033[31m'+str(numero_peca1)+'\033[0;0m')

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
                            sys.exit()
                    except:
                        qntd_velas = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[4]/th').text
                        if qntd_velas == 'Quantidade de velas':
                            qntd_velas1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody/tr[4]/td/span').text
                            #print('Quantidade de velas:', qntd_velas1)
                        else:
                            sys.exit()
                except:
                    qntd_velas = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[3]/th').text
                    if qntd_velas == 'Quantidade de velas':
                        qntd_velas1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[3]/td/span').text
                        #print('Quantidade de velas:',qntd_velas1)
                    else:
                        sys.exit()
            except:
                qntd_velas = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[4]/th').text
                if qntd_velas == 'Quantidade de velas':
                    qntd_velas1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[4]/td/span').text
                    #print('Quantidade de velas:',qntd_velas1)
                else:
                    sys.exit()
        except:
            qntd_velas = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[5]/th').text
            if qntd_velas == 'Quantidade de velas':
                qntd_velas1 = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[5]/td/span').text
                #print('Quantidade de velas:',qntd_velas1)
            else:
                sys.exit()
    except:
        qntd_velas1 = 'Não tem quantidade de velas'
        #print(f'\033[31m'+str(qntd_velas1)+'\033[0;0m')


    dicionario = {"titulo":titulo,
            "preco":preco.replace('\n', ''),
            "condicao":condicao,
            "qtd_vendida":vendas,
            "marca":marca1,
            # "linha": linha1,
            "modelo": modelo1,
            "numero_peca":numero_peca1,
            # "qntd_velas":qntd_velas1,
            "url": url,
    }

    with open(path_novo + "{}.txt".format(str(time.time()).replace('.', '')), 'w', encoding = 'utf-8') as f:
        f.write(json.dumps(dicionario))

    logging.info("Thread %s: finishing", d_aux)



if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    numero_drivers = 15
    
    # ---------------------------- lista de drivers
    dict_drivers = dict()
    for d in range(1, (numero_drivers+1)):
        logging.info("Driver %s", d)
        options = Options()
        options.headless = False
        dict_drivers[d] = webdriver.Firefox(options=options)

    # ---------------------------- ler urls sem titulo
    database = "db_anuncios_sonda_lambda.db"
    sql = "SELECT * FROM anuncios_sonda_lambda WHERE titulo IS NULL OR titulo = 'Não tem titulo'"
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute(sql)
    rows = c.fetchall()
    
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        #executor.submit(exec_scrapy, )
        futures = []
        for row in rows:
            futures.append(executor.submit(exec_scrapy, driver=, url=row[0]))
        for future in concurrent.futures.as_completed(futures):
            print('pending:', executor._work_queue.qsize(), 'jobs')
            print('threads:', len(executor._threads))
            print(future.result())
    """



    """
    pool = mpool.ThreadPool(10)
    d_aux = 1
    for row in rows:
        driver = dict_drivers.get(d_aux)
        pool.apply_async(exec_scrapy, args=(driver, row[0], ))

        if d_aux == 10:
            d_aux = 1
        elif d_aux == 1:
            d_aux += 1
        else:
            d_aux += 1
    """

    d_aux = 1
    with concurrent.futures.ThreadPoolExecutor(numero_drivers) as executor:
        for row in rows:
            driver = dict_drivers.get(d_aux)
            executor.submit(exec_scrapy, driver, row[0], d_aux)

            if d_aux == numero_drivers:
                d_aux = 1
            elif d_aux == 1:
                d_aux += 1
            else:
                d_aux += 1

"""
options = Options()
options.headless = False
driver = webdriver.Firefox(options=options)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    with concurrent.futures.ThreadPoolExecutor(10) as executor:
        # executor.submit(exec_scrapy, args=(driver, 'https://produto.mercadolivre.com.br/MLB-1871894340-reparo-completo-bico-injetor-ford-escort-18-16v-97-a-2002-_JM#position=3&search_layout=stack&type=item&tracking_id=2fabf431-d404-47d9-8f70-a58e9af524b8', 1, ))
        executor.submit(exec_scrapy, driver, 'https://produto.mercadolivre.com.br/MLB-1871894340-reparo-completo-bico-injetor-ford-escort-18-16v-97-a-2002-_JM#position=3&search_layout=stack&type=item&tracking_id=2fabf431-d404-47d9-8f70-a58e9af524b8', 1)


exec_scrapy(driver, 'https://produto.mercadolivre.com.br/MLB-1871894340-reparo-completo-bico-injetor-ford-escort-18-16v-97-a-2002-_JM#position=3&search_layout=stack&type=item&tracking_id=2fabf431-d404-47d9-8f70-a58e9af524b8', 1)
"""


""""
taskkill /F /IM firefox.exe /T
taskkill /F /IM geckodriver.exe /T
"""
