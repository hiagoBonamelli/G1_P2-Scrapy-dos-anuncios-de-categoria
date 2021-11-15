import sqlite3
import time

database = "db_anuncios_bico_injetor.db"
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

count = len(rows)
for row in rows:
    print(count)
    id_anuncio = "MLB" + row[1].split('-')[1]
    try:
        c.execute(sql, (id_anuncio, row[1], ))
        conn.commit()
    except:
        sql_delete = """DELETE
                        FROM anuncios
                        WHERE url  = ?
                    """
        c.execute(sql_delete, (row[1], ))
        conn.commit()
    
    count -= 1

# excluir sem id anuncio
# sql_excuir = 'DELETE FROM anuncios WHERE id_anuncio IS NULL;' 
# c.execute(sql_excuir)
# conn.commit()
