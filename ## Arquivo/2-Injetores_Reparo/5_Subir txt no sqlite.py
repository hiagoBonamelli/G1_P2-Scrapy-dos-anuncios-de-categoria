import sqlite3
import json
import os

database = "db_anuncios_injetores_reparo.db"
conn = sqlite3.connect(database)
c = conn.cursor()
path = "C:/Users/Hiago Bonomelli/Documents/aux_infos_injetores_reparo/"
lista_txt = os.listdir(path)

for txt in lista_txt:
    print(txt)
    with open(path + '{}'.format(txt), 'r') as fp:
        try:
            data = json.load(fp)
            
            # sql = ''' 
            # UPDATE anuncios
            # SET titulo = ?, 
                # preco = ?,
                # condicao = ?,
                # qtd_vendida = ?,
                # marca = ?,
                # modelo = ?,
                # numero_peca = ?,
                # id_anuncio = ?
            # WHERE URL = ?
            # '''


            # checkar se tem esse ID
            sql = 'SELECT * FROM anuncios WHERE id_anuncio  = ?'
            c.execute(sql, (data.get('id_anuncio'), ))
            rows = c.fetchall()

            if len(rows) == 0:
                sql = ''' 
                INSERT INTO anuncios (url, titulo, preco, condicao, qtd_vendida, marca, modelo, numero_peca, id_anuncio) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''

                c.execute(sql, (
                    data.get('url'),
                    data.get('titulo'),
                    data.get('preco'),
                    data.get('condicao'),
                    data.get('qtd_vendida'),
                    data.get('marca'),
                    data.get('modelo'),
                    data.get('numero_peca'),
                    data.get('id_anuncio')
                    )
                )
                conn.commit()

        except json.decoder.JSONDecodeError:
            pass

    os.remove(path + '{}'.format(txt))