import sqlite3
import json
import os

database = "db_anuncios_lampadas.db"
conn = sqlite3.connect(database)
c = conn.cursor()
path = "./4_excluir/"
lista_txt = os.listdir(path)

for txt in lista_txt:
    if txt.startswith("MLB"):
        id_anuncio = txt.replace('.txt', '')
    else:
        id_anuncio = "MLB" + txt.replace('.txt', '')
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