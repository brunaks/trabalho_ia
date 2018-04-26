
import nltk
import psycopg2
from nltk.corpus import wordnet

nltk.download('wordnet')

conn = psycopg2.connect("dbname='postgres' user='bruna'")

file  = open("Output.txt", "r");
lines = file.readlines()

text_file = open("Output-wordnet.txt", "w")
for line in lines:
    count = 0
    preprocessed_words = []
    potential_phrasal_verbs = []
    potential_phrasal_verb = None
    split_verb_and_prepositions = None

    split_line = line.split(',')
    source_file = split_line[0].split('\'')[1]
    id = split_line[1].split('\'')[0]
    split_line = split_line[2].split('\'')
    preprocessed_words.append(split_line[1])

    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM trabalho_ia.sentences WHERE source_file = %s AND id = %s""",
                   (source_file, str(id).strip()[0:-1]))
    rows = cursor.fetchall()

    potential_phrasal_verbs = []

    for preprocessed_word in preprocessed_words:
        split_verb_and_prepositions = preprocessed_word.split('_')

        potential_phrasal_verbs.append(split_verb_and_prepositions[0] + '_' + split_verb_and_prepositions[1])
        if len(split_verb_and_prepositions) > 2:
            potential_phrasal_verbs.append(split_verb_and_prepositions[0] + '_' + split_verb_and_prepositions[2])

            potential_phrasal_verbs.append(split_verb_and_prepositions[0] + '_' +
                                           split_verb_and_prepositions[1] + '_' +
                                           split_verb_and_prepositions[2])

    for potential_phrasal_verb in potential_phrasal_verbs:
        synsets = wordnet.synsets(potential_phrasal_verb)
        if len(synsets) > 0:
            sentence = ""
            for row in rows:
                sentence = sentence + row[2] + " "
            text_file.write(str((source_file, id, potential_phrasal_verb, sentence)))
            text_file.write("\n")

text_file.close()














