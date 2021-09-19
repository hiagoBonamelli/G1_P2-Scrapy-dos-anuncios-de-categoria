from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd

options = Options()
options.headless = False
driver = webdriver.Firefox(options=options)
driver.get("https://lista.mercadolivre.com.br/pecas/carros/injecao/sonda-lambda/_DisplayType_LF")

# pegar marcas
marcas = driver.find_elements_by_class_name("ui-search-search-modal-filter-name")
lista_marca_preco = []
for m in marcas:
    print(m.text)
    for i in range(1, 400):
        lista_marca_preco.append([i, m.text, "FAZER"])

df = pd.DataFrame(lista_marca_preco)
df.columns = ['preco', 'marca', 'status']
df.to_csv("1_df_lista_marca_preco.csv", index=False)
