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
        data = json.load(fp)
        
        sql = ''' 
        UPDATE anuncios
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