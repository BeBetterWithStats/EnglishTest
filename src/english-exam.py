
# coding: utf-8

# IMPORTS
import csv
import random
import os
# FIN -- IMPORTS


# METHODES
def list_files(folder_path):
	files = []
	for _path, _dirs, _files in os.walk(folder_path):
		for _file in _files:
			files.append(_file)
	return files


def type_an_answer(sentence):
	answer = input(sentence)
	return answer


def build_words_list(file, row):
	words = []
	with open(file, newline='') as csvfile:
		lines = csv.reader(csvfile, delimiter=';')
		for line in lines:
			words.append(line[row])
	return words
# FIN -- METHODES




# MAIN CODE
print("#############################################################")
print("################    ENGLISH VOCABULAR TEST   ################")
print("#############################################################")

LANGUE = ["EN", "FR"]
ROOT = "/Users/alexandrelods/Documents/Developpement/EnglishTest/files/"


# STEP 1 : select a file test

files = [x for x in list_files(ROOT) if str(x).endswith('.csv')]
sentence = "\n## STEP 1 ## Select a file :"
for f in files:
	sentence += "\n" + str(files.index(f)) + " : " + f
selected_file = type_an_answer(sentence + "\n>> ")

en_words = build_words_list(ROOT + files[int(selected_file)], LANGUE.index("EN"))
fr_words = build_words_list(ROOT + files[int(selected_file)], LANGUE.index("FR"))


# STEP 2 : test knowledge
score = 0

type_an_answer("\n## STEP 2 ## Are you ready ?")

for i in range(10):
	selected_language = random.randrange(len(LANGUE))
	selected_word = random.randrange(len(en_words))
	
	# if ENGLISH
	if (selected_language == LANGUE.index("EN")):

		sentence = "\nTranslate in french '" + en_words[selected_word] + "' :\n>> "
		answer = type_an_answer(sentence)
		if (answer.lower() == fr_words[selected_word].lower()):
			print("*** Yes !")
			score = score + 2
		elif (answer.lower() == 'help'):
			sentence = "it starts with a '" + fr_words[selected_word][0] + "' :\n>> "
			answer = type_an_answer(sentence)
			if (answer.lower() == fr_words[selected_word].lower()):
				print("*** Yes !")
				score = score + 1
			else:
				print("*** The answer was " + fr_words[selected_word])
		else:
			print("*** The answer was " + fr_words[selected_word])

	# if FRENCH
	elif (selected_language == LANGUE.index("FR")):
		
		sentence = "\nTranslate in english '" + fr_words[selected_word] + "' :\n>> "
		answer = type_an_answer(sentence)
		if (answer.lower() == en_words[selected_word].lower()):
			print("*** Yes !")
			score = score + 2
		elif (answer.lower() == 'help'):
			sentence = "it starts with a '" + en_words[selected_word][0] + "' :\n>> "
			answer = type_an_answer(sentence)
			if (answer.lower() == en_words[selected_word].lower()):
				print("*** Yes !")
				score = score + 1
			else:
				print("*** The answer was " + en_words[selected_word])
		else:
			print("*** The answer was " + en_words[selected_word])

	else:
		# exception coding error, these case will never happened
		print("[ERROR] language does not exist")

# STEP 3 : print score
print("\n\n## FINAL SCORE ## %d / 20\n\n" % score)

# FIN -- MAIN CODE