import psycopg2
import os

conn = psycopg2.connect("dbname='postgres' user='bruna'")

for source_file in os.listdir("wordLemPoS"):
    file = open("wordLemPoS/" + source_file)
    sentence_id = 1
    part = 1
    for line in file.readlines()[1:]:
        columns = line.split("\t")
        text = columns[0]
        lemma = columns[1]
        tag = columns[2].replace('\r\n', '')
        if text == '.':
            sentence_id += 1
            part = 1
        else:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO trabalho_ia.sentences " +
                               "(id, part, text, lemma, tag, source_file) " +
                               "VALUES (%s, %s, %s, %s, %s, %s)", (sentence_id, part, text, lemma, tag, source_file))
                conn.commit()
            except:
                conn = psycopg2.connect("dbname='postgres' user='bruna'")
            part += 1
