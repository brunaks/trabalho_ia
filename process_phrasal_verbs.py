import psycopg2
import os

conn = psycopg2.connect("dbname='postgres' user='bruna'")
cursor = conn.cursor()
cursor.execute("SELECT * FROM trabalho_ia.sentences LIMIT 10")
rows = cursor.fetchall()

for row in rows:
    sentence = row[1]
    index = sentence.find('_V')
    if index != -1:
        if sentence.find('_IN', index) != -1:
            print sentence
            print '\n'
