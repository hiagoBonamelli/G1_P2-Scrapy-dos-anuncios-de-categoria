import sqlite3
import json
import os

database = "db_anuncios_sonda_lambda.db"
conn = sqlite3.connect(database)
c = conn.cursor()
path = "C:/Users/Hiago Bonomelli/Documents/aux_infos/"
# path = 'C:/Users/dell/Documents/aux_infos/'
lista_txt = os.listdir(path)

for txt in lista_txt:
    print(txt)
    try:
        with open(path + '{}'.format(txt), 'r') as fp:
            data = json.load(fp)
            
            sql = ''' 
            UPDATE anuncios_sonda_lambda
            SET titulo = ?, 
                preco = ?,
                condicao = ?,
                qtd_vendida = ?,
                marca = ?,
                modelo = ?,
                numero_peca = ?
            WHERE URL = ?
            '''

            c.execute(sql, (
                data.get('titulo'),
                data.get('preco'),
                data.get('condicao'),
                data.get('qtd_vendida'),
                data.get('marca'),
                data.get('modelo'),
                data.get('numero_peca'),
                data.get('url'),
                )
            )
            conn.commit()

        os.remove(path + '{}'.format(txt))

    except:
        pass