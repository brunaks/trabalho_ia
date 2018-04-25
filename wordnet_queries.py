import nltk
from nltk.corpus import wordnet

nltk.download('wordnet')

file  = open("Output.txt", "r");
lines = file.readlines()

phrasal_verbs = []
for line in lines:
    count = 0
    preprocessed_words = []
    potential_phrasal_verbs = []
    potential_phrasal_verb = None
    splitted_verb_and_prepositions = None

    splitted_line = line.split(',')
    splitted_line = splitted_line[2].split('\'')
    preprocessed_words.append(splitted_line[1])

    potential_phrasal_verbs = []

    for preprocessed_word in preprocessed_words:
        splitted_verb_and_prepositions = preprocessed_word.split('_')

        potential_phrasal_verbs.append(splitted_verb_and_prepositions[0] + '_' + splitted_verb_and_prepositions[1])
        if len(splitted_verb_and_prepositions) > 2:
            potential_phrasal_verbs.append(splitted_verb_and_prepositions[0] + '_' + splitted_verb_and_prepositions[2])

            potential_phrasal_verbs.append(splitted_verb_and_prepositions[0] + '_' +
                                             splitted_verb_and_prepositions[1] + '_' +
                                             splitted_verb_and_prepositions[2])

    for potential_phrasal_verb in potential_phrasal_verbs:
        synsets = wordnet.synsets(potential_phrasal_verb)
        if len(synsets) > 0:
            phrasal_verbs.append((line, potential_phrasal_verb))
            print(line + " " + potential_phrasal_verb)

    count = count + 1
    print(count)

text_file = open("Output-wordnet.txt", "w")
for phrasal_verb in phrasal_verbs:
    text_file.write(str(phrasal_verb))
    text_file.write("\n")
text_file.close()














