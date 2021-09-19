from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd

# configuracoes iniciais
url = "https://lista.mercadolivre.com.br/pecas/carros/injecao/injetores/reparo_DisplayType_LF_PriceRange_{inicial}-{final}"
path_bases = "./bases/"

options = Options()
options.headless = False
driver = webdriver.Firefox(options=options)
driver.get("https://www.mercadolivre.com.br/")
driver.get("https://www.mercadolivre.com.br/apple-iphone-12-128-gb-branco/p/MLB16163652")
driver.find_element_by_xpath('//*[@id="newCookieDisclaimerButton"]').click()





# funcao pra pegar os links de uma pagina e salvar um csv
def get_urls_page(driver, num_page, i, j):
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
    df.to_csv(path_bases + "df_lista_precos_" + str(i) + "_" + str(j) + "_" + "page_" + str(num_page) + ".csv")






def iter_pages(driver, i, j):
    # identificar numero de paginas
    try:
        xpath_num_paginas = "/html/body/main/div/div[1]/section/div[3]/ul/li[2]"
        elem_num_paginas = driver.find_element_by_xpath(xpath_num_paginas)
        elem_num_paginas = int(elem_num_paginas.text.split(" ")[1])
    except:
        elem_num_paginas = 0
    
    if elem_num_paginas == 0:
        get_urls_page(driver, 0, i, j)
    else:
        for num_page in range(1, int(elem_num_paginas)+1):
            get_urls_page(driver, num_page, i, j)
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
            




df_lista_precos = pd.read_csv("1_df_lista_precos.csv")
df_lista_precos = df_lista_precos[df_lista_precos["status"] != "OK"]

for index, row in df_lista_precos.iterrows():
    # abrir url
    i = str(row['precos'])
    f = str(int(float(i)) + 1)
    url_get = url.format(
        inicial = i,
        final = f
    )
    driver.get(url_get)
    
    # verificar sem tem algum resultado
    try:
        elem_busca = driver.find_element_by_xpath("/html/body/main/div/div/div[2]/h3").text
    except:
        elem_busca = ""
    
    if elem_busca == 'Não há anúncios que correspondem à sua busca.':
        print(i + "-" + f + " - " + "Sem resultado")
    else:   
        iter_pages(driver, i, f)
        print(i + "-" + f + " - ")
        
    df_lista_precos.at[index, 'status'] = "OK"
    df_lista_precos.to_csv("1_df_lista_precos.csv", index=False)