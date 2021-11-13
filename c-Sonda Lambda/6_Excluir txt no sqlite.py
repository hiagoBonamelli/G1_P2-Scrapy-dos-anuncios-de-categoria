import sqlite3
import json
import os

database = "db_anuncios_sonda_lambda.db"
conn = sqlite3.connect(database)
c = conn.cursor()
path = "./4_excluir/"
lista_txt = os.listdir(path)

for txt in lista_txt:
    id_anuncio = txt.replace('.txt', '')
    print(id_anuncio)

    sql_delete = '''
        DELETE FROM anuncios
        WHERE id_anuncio = ?;
    '''

    c.execute(sql_delete, (
        id_anuncio,
        )
    )
    conn.commit()

    os.remove(path + '{}'.format(txt))