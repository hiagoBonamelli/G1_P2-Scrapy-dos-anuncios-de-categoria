from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import logging
import pandas as pd

# configuracoes iniciais
# url = "https://lista.mercadolivre.com.br/pecas/carros/injecao/injetores/reparo_DisplayType_LF_PriceRange_{inicial}-{final}"
# url = "https://lista.mercadolivre.com.br/pecas/carros/injecao/sonda-lambda/{marca}/_DisplayType_LF_PriceRange_{inicial}-{final}"
url = "https://lista.mercadolivre.com.br/pecas/carros/motor/radiadores/tampa-radiador/{marca}/_DisplayType_LF_PriceRange_{inicial}-{final}"
# url = "http://api.scraperapi.com?api_key=a1f5eae4966a5e0e09ec7d83b2f3819e&url=https://lista.mercadolivre.com.br/pecas/carros/injecao/sonda-lambda/{marca}/_DisplayType_LF_PriceRange_{inicial}-{final}"

path_bases = "C:/Users/Hiago Bonomelli/Documents/aux_links/"
# path_bases = "C:/Users/Hiago Bonomelli/Documents/auxiliares/"
# path_bases = "C:/Users/dell/Documents/Auxiliares/"


options = Options()
options.headless = False
driver = webdriver.Firefox(options=options)
driver.get("https://www.mercadolivre.com.br/")
try:
    driver.find_element_by_xpath('//*[@id="newCookieDisclaimerButton"]').click()
except:
    pass




# funcao pra pegar os links de uma pagina e salvar um csv
def get_urls_page(driver, m, num_page, i, j):
    lista_urls = []
    num_anuncios = len(driver.find_elements_by_class_name('ui-search-layout__item'))
    
    for u in range(1, num_anuncios+1):
        xpath_url = "/html/body/main/div/div[1]/section/ol/li[{}]/div/div/div[2]/div[1]/a"
        xpath_url_mais_vendido = "/html/body/main/div/div[1]/section/ol/li[{}]/div/div/div[2]/div[2]/a"

        aux_url_anuncio = 0
        while aux_url_anuncio == 0:
            try:
                elem_url = driver.find_element_by_xpath(xpath_url.format(str(u)))
                url_anuncio = elem_url.get_attribute("href")
                aux_url_anuncio += 1
            except:
                try:
                    elem_url = driver.find_element_by_xpath(xpath_url_mais_vendido.format(str(u)))
                    url_anuncio = elem_url.get_attribute("href")
                    aux_url_anuncio += 1
                except:
                    pass

        lista_urls.append(url_anuncio)
        
    df = pd.DataFrame({'urls':lista_urls})
    df.to_csv(path_bases + "df_lista_precos_" + m + "_" + str(i) + "_" + str(j) + "_" + "page_" + str(num_page) + ".csv")






def iter_pages(driver, m, i, j):
    # identificar numero de paginas
    try:
        xpath_num_paginas = "/html/body/main/div/div[1]/section/div[3]/ul/li[2]"
        elem_num_paginas = driver.find_element_by_xpath(xpath_num_paginas)
        elem_num_paginas = int(elem_num_paginas.text.split(" ")[1])
    except:
        elem_num_paginas = 0
    
    if elem_num_paginas == 0:
        get_urls_page(driver, m, 0, i, j)
        time.sleep(2)
    else:
        for num_page in range(1, int(elem_num_paginas)+1):
            get_urls_page(driver, m, 0, i, j)
            time.sleep(2)
            if num_page == elem_num_paginas:
                pass
            else:
                aux_proxima_pagina = 0
                i_aux = time.time()
                while aux_proxima_pagina == 0:
                    try:
                        driver.find_element_by_xpath("/html/body/main/div/div[1]/section/div[3]/ul/li[3]/a").click()
                        aux_proxima_pagina += 1
                    except:
                        try:
                            driver.find_element_by_xpath('/html/body/main/div/div[1]/section/div[3]/ul/li[4]/a').click()
                            aux_proxima_pagina += 1
                        except:
                            pass
                        aux_proxima_pagina += 1
                    if (time.time() - i_aux) >= 4:
                        driver.refresh()
                        i_aux = time.time() 
                    
    del elem_num_paginas
            




df_lista_marca_preco = pd.read_csv("1_df_lista_marca_preco.csv")
df_lista_marca_preco = df_lista_marca_preco[df_lista_marca_preco["status"] != "OK"]


tamanho = len(df_lista_marca_preco)

for index, row in df_lista_marca_preco.iterrows():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    # print(tamanho)
    logging.info("Tamanho %s", tamanho)
    # abrir url
    i = str(row['preco'])
    f = str(int(float(i)) + 1)
    m = row['marca']
    url_get = url.format(
        marca = m,
        inicial = i,
        final = f,
    )
    aux_get = 0
    while aux_get == 0:
        try:
            driver.get(url_get)
            aux_get += 1
        except:
            pass
    
    # verificar sem tem algum resultado
    try:
        elem_busca = driver.find_element_by_xpath("/html/body/main/div/div/div[2]/h3").text
    except:
        elem_busca = ""
    
    if elem_busca == 'Não há anúncios que correspondem à sua busca.':
        # print(i + "-" + f + " - " + "Sem resultado")
        logging.info("%s-%s - Sem resultado", i, f)
    else:   
        iter_pages(driver, m, i, f)
        # print(i + "-" + f + " - ")
        logging.info("%s-%s", i, f)
        
    df_lista_marca_preco.at[index, 'status'] = "OK"
    aux_excel = 0
    while aux_excel == 0:
        try:
            df_lista_marca_preco.to_csv("1_df_lista_marca_preco.csv", index=False)
            aux_excel += 1
        except:
            pass
    tamanho -= 1