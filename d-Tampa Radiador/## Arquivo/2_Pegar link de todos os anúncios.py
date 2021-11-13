from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import sys
import pandas as pd
import logging
from urllib.parse import urlencode
from selenium.common.exceptions import TimeoutException


# configuracoes iniciais
url = "https://lista.mercadolivre.com.br/pecas/carros/injecao/sonda-lambda/{marca}/_DisplayType_LF_PriceRange_{inicial}-{final}"
path_bases = "./2_bases/"

options = Options()
options.headless = False
driver = webdriver.Firefox(options=options)
driver.get("https://www.mercadolivre.com.br/")
driver.get("https://www.mercadolivre.com.br/apple-iphone-12-128-gb-branco/p/MLB16163652")
driver.find_element_by_xpath('//*[@id="newCookieDisclaimerButton"]').click()





# funcao pra pegar os links de uma pagina e salvar um csv
def get_urls_page(driver, num_page, i, j, m):
    lista_urls = []
    aux_num_anuncios = 0
    while aux_num_anuncios >= 0:
        try:
            num_anuncios = len(driver.find_elements_by_class_name('ui-search-layout__item'))
            aux_num_anuncios = -1
        except:
            logging.info("Tentativa num_anuncios %s", aux_num_anuncios)
            aux_num_anuncios += 1
        
    logging.info("Passar paginas")
    for u in range(1, num_anuncios+1):
        xpath_url = "/html/body/main/div/div[1]/section/ol/li[{}]/div/div/div[2]/div[1]/a"
        xpath_url_mais_vendido = "/html/body/main/div/div[1]/section/ol/li[{}]/div/div/div[2]/div[2]/a"
        xpath_url2 = '/html/body/main/div/div[1]/section/ol/li[{}]/div/div/div[2]/div[1]/a'

        try:
            elem_url = driver.find_element_by_xpath(xpath_url.format(str(u)))
            url_anuncio = elem_url.get_attribute("href")
        except:
            try:
                elem_url = driver.find_element_by_xpath(xpath_url_mais_vendido.format(str(u)))
                url_anuncio = elem_url.get_attribute("href")
            except:
                elem_url = driver.find_element_by_xpath(xpath_url2.format(str(u)))
                url_anuncio = elem_url.get_attribute("href")

        lista_urls.append(url_anuncio)
        
    df = pd.DataFrame({'urls':lista_urls})
    df.to_csv(path_bases + "df_lista_precos_" + str(m) + '_' + str(i) + "_" + str(j) + "_" + "page_" + str(num_page) + ".csv")






def iter_pages(driver, i, j, m):
    # identificar numero de paginas
    try:
        xpath_num_paginas = "/html/body/main/div/div[1]/section/div[3]/ul/li[2]"
        elem_num_paginas = driver.find_element_by_xpath(xpath_num_paginas)
        elem_num_paginas = int(elem_num_paginas.text.split(" ")[1])
    except:
        elem_num_paginas = 0
    
    if elem_num_paginas == 0:
        get_urls_page(driver, 0, i, j, m)
        time.sleep(2)
    else:
        for num_page in range(1, int(elem_num_paginas)+1):
            get_urls_page(driver, num_page, i, j, m)
            time.sleep(2)
            if num_page == elem_num_paginas:
                pass
            else:
                try:
                    try:
                        driver.find_element_by_xpath("/html/body/main/div/div[1]/section/div[3]/ul/li[3]/a").click()
                    except:
                        driver.find_element_by_xpath('/html/body/main/div/div[1]/section/div[3]/ul/li[4]/a').click()
                except:
                    driver.refresh()
                    time.sleep(5)
            

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")


df_lista_precos = pd.read_csv("1_df_lista_marca_preco.csv")
df_lista_precos = df_lista_precos[df_lista_precos["status"] != "OK"]
logging.info("Total %s", len(df_lista_precos))

for index, row in df_lista_precos.iterrows():
    # abrir url
    i = str(row['preco'])
    f = str(int(float(i)) + 1)
    m = row['marca']
    url_get = url.format(
        marca = m,
        inicial = i,
        final = f
    )
    try:
        driver.get(url_get)
    except TimeoutException as e:
        driver.get(url_get)
    time.sleep(2)
    
    # verificar sem tem algum resultado
    try:
        elem_busca = driver.find_element_by_xpath("/html/body/main/div/div/div[2]/h3").text
    except:
        elem_busca = ""
    
    if elem_busca == 'Não há anúncios que correspondem à sua busca.':
        logging.info("%s - %s - %s - Sem resultado", i, f, m)
        # sprint(i + "-" + f + " - " + m + " - " + " - Sem resultado")
    else:   
        iter_pages(driver, i, f, m)
        logging.info("%s - %s - %s", i, f, m)
        #print(i + "-" + f + " - " + m)
        
    df_lista_precos.at[index, 'status'] = "OK"
    df_lista_precos.to_csv("1_df_lista_marca_preco.csv", index=False)

