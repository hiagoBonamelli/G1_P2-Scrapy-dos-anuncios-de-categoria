import sqlite3
import numpy as np
import pandas as pd

database = "db_anuncios_bico_injetor.db"
sql = """
SELECT * 
FROM anuncios 
WHERE (titulo IS NULL) 
OR (titulo = 'Não tem titulo') 
OR (preco = 'não tem preço') 
OR (condicao = 'Nao tem condicao') 
OR (qtd_vendida = 'Não tem qntd de vendas') 
OR (condicao <> 'Novo' AND condicao <> 'Usado' AND condicao <> 'Recondicionado')

"""
# sql = " SELECT * FROM anuncios "
conn = sqlite3.connect(database)

df = pd.read_sql_query(sql, conn)
print(len(df))
df['status'] = 'FAZER'

list_df = np.array_split(df, 20)
count = 1
for df_aux in list_df:
    df_aux.to_csv('./4_lista_df/df' + str(count) + '.csv')
    count += 1
