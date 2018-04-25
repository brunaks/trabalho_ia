import psycopg2
from itertools import islice
import time


class Extractor:
    def extract_phrasal_verbs(self, rows):
        phrasal_verbs = []
        current_index = 0L
        for row in rows:
            current_lemma = row[3]
            current_tag = row[4]

            if self.is_verb(current_tag) and (len(rows) > current_index + 1) and (row[0] == rows[current_index + 1][0]):
                end_index = self.get_index_of_next_verb_in_same_sentence(rows, current_index + 1)
                phrasal_verb = self.extract_phrasal_verb(current_lemma, rows, current_index + 1, end_index)
                if phrasal_verb is not None:
                    phrasal_verbs.append(phrasal_verb)

            current_index += 1
        return phrasal_verbs

    def get_index_of_next_verb_in_same_sentence(self, rows, start_index):
        last_sentence_id = None
        end_index = start_index
        for row in islice(rows, start_index, None):
            current_sentence_id = row[0]
            if self.is_verb(row[4]) or (last_sentence_id is not None and current_sentence_id != last_sentence_id):
                return end_index + 1
            last_sentence_id = current_sentence_id
            end_index += 1

        return None

    def extract_phrasal_verb(self, verb, rows, start_index, end_index):
        found_one = False
        first_found = None
        for row in islice(rows, start_index, end_index):
            current_id = row[0]
            current_word = row[2]

            if self.is_preposition(row):
                if found_one:
                    return row[5], current_id, verb + "_" + first_found + "_" + current_word
                else:
                    found_one = True
                    first_found = current_word

        if found_one:
            return row[5], current_id, verb + "_" + first_found
        else:
            return None

    def is_preposition(self, row):
        return len(row[4]) > 0 and (row[4][0:2] == 'rp' or row[4][0] == 'i') and row[2] != '@'

    def is_verb(self, tag):
        return len(tag) > 0 and tag[0] == 'v'


def test(description, rows, expected):
    extended_rows = []
    for row in rows:
        extended_rows.append((row[0], row[1], row[2], row[3], row[4], ''));

    extended_expected_rows = []
    for row in expected:
        extended_expected_rows.append(('', row[0], row[1]));

    result = Extractor().extract_phrasal_verbs(extended_rows)
    if result == extended_expected_rows:
        print description + ": OK"
    else:
        print description + ":\n" + str(result) + " is not equal " + str(extended_expected_rows)


print 'verb'[0]

test("with verb without preposition", [
    (1L, 1L, 'i', 'i', 'nonimportant'),
    (1L, 2L, 'help', 'help', 'verb'),
    (1L, 3L, 'mumu', 'mumu', 'nonimportant')
], [])

for preposition_type in ["rp", "ii"]:
    test("without verb with preposition " + preposition_type, [
        (1L, 1L, 'i', 'i', 'nonimportant'),
        (1L, 2L, 'mumu', 'mumu', preposition_type)
    ], [])

    test("with only a phrasal verb with " + preposition_type, [
        (1L, 1L, 'help', 'help', 'verb'),
        (1L, 2L, 'out', 'out', preposition_type)
    ], [(1L, "help_out")])

    test("with only two phrasal verbs with " + preposition_type, [
        (1L, 1L, 'help', 'help', 'verb'),
        (1L, 2L, 'out', 'out', preposition_type),
        (1L, 3L, 'got', 'got', 'verb'),
        (1L, 4L, 'out', 'out', preposition_type)
    ], [(1L, "help_out"), (1L, "got_out")])

    test("with only second phrasal verbs valid with " + preposition_type, [
        (1L, 1L, 'help', 'help', 'verb'),
        (1L, 2L, 'me', 'me', 'nonimportant'),
        (1L, 3L, 'got', 'got', 'verb'),
        (1L, 4L, 'out', 'out', preposition_type)
    ], [(1L, "got_out")])

    test("with a word before the phrasal verb with " + preposition_type, [
        (1L, 1L, 'i', 'i', 'nonimportant'),
        (1L, 2L, 'help', 'help', 'verb'),
        (1L, 3L, 'out', 'out', preposition_type)
    ], [(1L, "help_out")])

    test("with a word after the phrasal verb with " + preposition_type, [
        (1L, 1L, 'help', 'help', 'verb'),
        (1L, 2L, 'out', 'out', preposition_type),
        (1L, 3L, 'mumu', 'mumu', 'nonimportant')
    ], [(1L, "help_out")])

    test("with a word in the middle the phrasal verb with " + preposition_type, [
        (1L, 1L, 'help', 'help', 'verb'),
        (1L, 2L, 'you', 'you', 'nonimportant'),
        (1L, 3L, 'out', 'out', preposition_type),
    ], [(1L, "help_out")])

    test("with many words in the middle the phrasal verb with " + preposition_type, [
        (1L, 1L, 'help', 'help', 'verb'),
        (1L, 2L, 'the', 'the', 'nonimportant'),
        (1L, 3L, 'cutest', 'cutest', 'nonimportant'),
        (1L, 4L, ',', ',', 'nonimportant'),
        (1L, 5L, 'most', 'most', 'nonimportant'),
        (1L, 6L, 'amazing', 'amazing', 'nonimportant'),
        (1L, 7L, 'and', 'and', 'nonimportant'),
        (1L, 8L, 'loving', 'loving', 'nonimportant'),
        (1L, 9L, 'mumu', 'mumu', 'nonimportant'),
        (1L, 10L, 'out', 'out', preposition_type),
    ], [(1L, "help_out")])

    test("a phrasal verb with two prepositions with  " + preposition_type, [
        (1L, 1L, 'put', 'put', 'verb'),
        (1L, 2L, 'up', 'up', preposition_type),
        (1L, 3L, 'with', 'with', preposition_type),
    ], [(1L, "put_up_with")])

    test("phrasal verb at sentence break with  " + preposition_type, [
        (1L, 1L, 'put', 'put', 'verb'),
        (2L, 1L, 'up', 'up', preposition_type),
        (2L, 1L, 'with', 'with', preposition_type),
    ], [])

    test("acceptance test with " + preposition_type, [
        (1L, 1L, 'she', 'she', 'nonimportant'),
        (1L, 2L, 'helped', 'help', 'verb'),
        (1L, 3L, 'me', 'me', 'nonimportant'),
        (1L, 4L, 'to', 'to', preposition_type),
        (1L, 5L, 'get', 'get', 'verb'),
        (1L, 6L, 'out', 'out', preposition_type),
        (1L, 7L, 'of', 'of', preposition_type),
        (1L, 8L, 'prison', 'prison', 'nonimportant'),
        (1L, 9L, 'and', 'and', 'nonimportant'),
        (1L, 10L, 'now', 'now', 'nonimportant'),
        (1L, 11L, 'i', 'i', 'nonimportant'),
        (1L, 12L, 'have', 'have', 'verb'),
        (1L, 13L, 'to', 'to', preposition_type),
        (1L, 14L, 'put', 'put', 'verb'),
        (1L, 15L, 'up', 'up', preposition_type),
        (1L, 16L, 'with', 'with', preposition_type),
        (1L, 17L, 'her', 'her', 'nonimportant'),
    ], [
             (1L, "help_to"),
             (1L, "get_out_of"),
             (1L, "have_to"),
             (1L, "put_up_with")
         ])

    test("acceptance test with two phrases with " + preposition_type, [
        (1L, 1L, 'she', 'she', 'nonimportant'),
        (1L, 2L, 'helped', 'help', 'verb'),
        (1L, 3L, 'me', 'me', 'nonimportant'),
        (1L, 4L, 'to', 'to', preposition_type),
        (1L, 5L, 'get', 'get', 'verb'),
        (1L, 6L, 'out', 'out', preposition_type),
        (1L, 7L, 'of', 'of', preposition_type),
        (1L, 8L, 'prison', 'prison', 'nonimportant'),
        (2L, 1L, 'now', 'now', 'nonimportant'),
        (2L, 2L, 'i', 'i', 'nonimportant'),
        (2L, 3L, 'have', 'have', 'verb'),
        (2L, 4L, 'to', 'to', preposition_type),
        (2L, 5L, 'put', 'put', 'verb'),
        (2L, 6L, 'up', 'up', preposition_type),
        (2L, 7L, 'with', 'with', preposition_type),
        (2L, 8L, 'her', 'her', 'nonimportant'),
    ], [
             (1L, "help_to"),
             (1L, "get_out_of"),
             (2L, "have_to"),
             (2L, "put_up_with")
         ])

conn = psycopg2.connect("dbname='postgres' user='bruna'")
cursor = conn.cursor()
cursor.execute("select distinct(source_file) from trabalho_ia.sentences")
source_files = cursor.fetchall()

allResults = []
for source_file in source_files:
    print source_file[0]
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trabalho_ia.sentences WHERE source_file = %s ORDER BY id ASC, part ASC ",
                   source_file)
    rows = cursor.fetchall()
    print 'Data selected, count is: ' + str(len(rows))

    print str(time.time())
    results = Extractor().extract_phrasal_verbs(rows)
    print str(time.time())
    print 'Phrasal verbs extracted, count is: ' + str(len(results))
    allResults.extend(results)

text_file = open("Output.txt", "w")
for row in allResults:
    text_file.write(str(row))
    text_file.write("\n")
text_file.close()
