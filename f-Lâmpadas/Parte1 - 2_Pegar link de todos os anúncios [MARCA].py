from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import sys
import os
import pandas as pd
from urllib.parse import urlencode

API_KEY = "a1f5eae4966a5e0e09ec7d83b2f3819e"


def get_scraperapi_url(url):
    """
        Converts url into API request for ScraperAPI.
    """
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    # proxy_url = url
    return proxy_url



# configuracoes iniciais
url = "https://lista.mercadolivre.com.br/pecas/carros/iluminacao/lampadas/{marca}/_DisplayType_LF_PriceRange_{inicial}-{final}_NoIndex_True"
path_bases = "./2_bases/"

options = Options()
options.headless = False
driver = webdriver.Firefox(options=options)
driver.get(get_scraperapi_url("https://www.mercadolivre.com.br/"))
driver.get(get_scraperapi_url("https://www.mercadolivre.com.br/apple-iphone-12-128-gb-branco/p/MLB16163652"))
driver.find_element_by_xpath('//*[@id="newCookieDisclaimerButton"]').click()





# funcao pra pegar os links de uma pagina e salvar um csv
def get_urls_page(driver, num_page, i, j, m):
    lista_urls = []
    num_anuncios = len(driver.find_elements_by_class_name('ui-search-layout__item'))
    
    for u in range(1, num_anuncios+1):
        xpath_url = "/html/body/main/div/div[1]/section/ol/li[{}]/div/div/div[2]/div[1]/a"
        xpath_url_mais_vendido = "/html/body/main/div/div[1]/section/ol/li[{}]/div/div/div[2]/div[2]/a"

        try:
            elem_url = driver.find_element_by_xpath(xpath_url.format(str(u)))
            url_anuncio = elem_url.get_attribute("href")
        except:
            elem_url = driver.find_element_by_xpath(xpath_url_mais_vendido.format(str(u)))
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
                    aux_refresh = 0
                    while aux_refresh == 0:
                        try:
                            driver.refresh()
                            time.sleep(5)
                            aux_refresh = 1
                        except:
                            pass
            



path = './1_bases/'
df_lista_precos = pd.read_csv(path + sys.argv[1])
df_lista_precos = df_lista_precos[df_lista_precos["status"] != "OK"]

# selecionar marca
# lista_marca = list(set(df_lista_precos['marca']))
# aux_marca = sys.argv[1]
# marca_selecionada = lista_marca[int(aux_marca)]
# df_lista_precos = df_lista_precos[df_lista_precos['marca'] == marca_selecionada]

vez = 1

while len(df_lista_precos) > 0:
    df_lista_precos = pd.read_csv(path + sys.argv[1])
    df_lista_precos = df_lista_precos[df_lista_precos["status"] != "OK"]

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
        
        # fazer get até dar certo
        aux_get = 0
        while aux_get == 0:
            try:
                driver.get(get_scraperapi_url(url_get))
                aux_get = 1
            except:
                pass

        body = driver.find_element_by_xpath('/html/body').text
        
        if '"type":"Buffer","data":' in body:
            print("Erro na requisição")

        else:
            try:
                elem_busca = driver.find_element_by_xpath("/html/body/main/div/div/div[2]/h3").text
            except:
                elem_busca = ""
            
            if elem_busca == 'Não há anúncios que correspondem à sua busca.':
                print(i + "-" + f + " - " + m + " - " + " - Sem resultado")
            else:   
                iter_pages(driver, i, f, m)
                print(i + "-" + f + " - " + m)
                
            df_lista_precos.at[index, 'status'] = "OK"
            df_lista_precos.to_csv(path + sys.argv[1], index=False)

driver.quit()
os.remove(path + sys.argv[1])