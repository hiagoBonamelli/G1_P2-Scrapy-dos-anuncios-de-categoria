from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import numpy as np

options = Options()
options.headless = False
driver = webdriver.Firefox(options=options)
driver.get("https://lista.mercadolivre.com.br/pecas/carros/iluminacao/lampadas/_DisplayType_LF_NoIndex_True")

# pegar cidades
cidades = driver.find_elements_by_class_name("ui-search-search-modal-filter-name")
lista_cidades_preco = []
for m in cidades:
    print(m.text)
    for i in range(1, 1000):
        lista_cidades_preco.append([i, m.text, "FAZER"])

df = pd.DataFrame(lista_cidades_preco)
df.columns = ['preco', 'cidade', 'status']
# df.to_csv("lista_cidades_preco.csv", index=False)


""" # -------------- ler o df 
df = pd.read_csv("lista_cidades_preco.csv")
df = df[df["status"] != "OK"]
"""

# dividir em dfs de 50
list_df = np.array_split(df, 20)

count = 1
for df_aux in list_df:
    df_aux.to_csv('./1_bases/df' + str(count) + '.csv')
    count += 1
