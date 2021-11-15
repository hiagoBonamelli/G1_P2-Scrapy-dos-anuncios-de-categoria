import os
import sqlite3
import pandas as pd

path = "./2_bases/"
files = os.listdir(path)
df = pd.DataFrame()

for f in files:
    df_aux = pd.read_csv(path + f, index_col=0)
    df = df.append(df_aux)
    print(len(df))



sql_create_anuncios_table = '''CREATE TABLE IF NOT EXISTS anuncios (
    id_anuncio text PRIMARY KEY,
    url text, 
    titulo text, 
    preco text, 
    condicao text, 
    qtd_vendida text, 
    marca text, 
    modelo text, 
    numero_peca text 
)
'''

database = "db_anuncios_bico_injetor.db"
conn = sqlite3.connect(database)
c = conn.cursor()
c.execute(sql_create_anuncios_table)

# adicionar dados
sql = ''' INSERT OR IGNORE INTO anuncios(url)
                    VALUES(?) '''

tamanho = len(df)
for index, row in df.iterrows():
    if 'click1' in row['urls']:
        pass
    else:
        anuncio = (row['urls'],)
        c.execute(sql, anuncio)
        conn.commit()
    tamanho -= 1
    print(tamanho)

# excluir arquivos
for f in files:
    os.remove(path + f)