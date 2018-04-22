import psycopg2
import os

conn = psycopg2.connect("dbname='postgres' user='bruna'")

for source_file in os.listdir("wordLemPoS"):
    file = open("wordLemPoS/" + source_file)
    sentences = file.read().split('.')
    for sentence in sentences:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO trabalho_ia.sentences (text, source_file) VALUES (%s, %s)", (sentence, source_file))
conn.commit()

# cursor = conn.cursor()
# cursor.execute("""SELECT * FROM trabalho_ia.sentences""")
# rows = cursor.fetchall()
# for row in rows:
#     print row
