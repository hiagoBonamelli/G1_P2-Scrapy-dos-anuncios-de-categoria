import sqlite3

database = "db_anuncios_injetores_reparo.db"
sql = "SELECT * FROM anuncios WHERE id_anuncio IS NULL"
conn = sqlite3.connect(database)
c = conn.cursor()
c.execute(sql)
rows = c.fetchall()

# sql = ''' 
#         INSERT INTO anuncios (id_anuncio) 
#         VALUES (?)
#     '''

sql = '''
        UPDATE anuncios SET id_anuncio = ? WHERE url = ?
'''

for row in rows:
    print(row[1])
    id_anuncio = "MLB" + row[1].split('-')[1]
    try:
        c.execute(sql, (id_anuncio, row[1], ))
        conn.commit()
    except:
        pass
        

# excluir sem id anuncio
sql_excuir = 'DELETE FROM anuncios WHERE id_anuncio IS NULL;' 
c.execute(sql_excuir)
conn.commit()
