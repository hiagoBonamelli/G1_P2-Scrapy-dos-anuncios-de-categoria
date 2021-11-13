import sqlite3
import json
import os

database = "db_anuncios_tampa_radiador.db"
conn = sqlite3.connect(database)
c = conn.cursor()
path = "./4_bases_anuncios/"
lista_txt = os.listdir(path)

for txt in lista_txt:
    print(txt)
    with open(path + '{}'.format(txt), 'r') as fp:
        try:
            data = json.load(fp)

            sql_insert = '''
            INSERT INTO anuncios (url, titulo, preco, condicao, qtd_vendida, numero_peca, id_anuncio)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            '''

            sql_update = '''
            UPDATE anuncios
            SET url = ?,
                titulo = ?,
                preco = ?,
                condicao = ?,
                qtd_vendida = ?,
                marca = ?
            WHERE id_anuncio = ?
            '''

            # verificar se o id começa com MLB
            id_anuncio = data.get('id_anuncio')
            if id_anuncio.startswith("MLB"):
                pass
            else:
                id_anuncio = "MLB" + id_anuncio

            c.execute(sql_update, (
                data.get('url'),
                data.get('titulo'),
                data.get('preco'),
                data.get('condicao'),
                data.get('qtd_vendida'),
                data.get('marca'),
                # data.get('modelo'),
                # data.get('numero_peca'),
                id_anuncio
                )
            )
            conn.commit()

        except json.decoder.JSONDecodeError:
             pass

    os.remove(path + '{}'.format(txt))