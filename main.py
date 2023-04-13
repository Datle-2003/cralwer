import psycopg2
import urllib.parse as urlparse

conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='Data',
            user='postgres',
            password='123',
            client_encoding='UTF8'
        ) 
cur = conn.cursor()
cur.execute(""" DROP TABLE items
""")

conn.commit()

cur.close()
conn.close()
