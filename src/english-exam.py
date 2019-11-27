
# coding: utf-8

# IMPORTS
import csv
import random
# FIN -- IMPORTS


# METHODES
def type_an_answer(word, language):
	answer = input("\n>> Translate " + word + " (" + LANGUE[language] + ")" " : ")
	# print("Vous avez tapé " + answer)
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

en_words = build_words_list('/Users/alexandrelods/Documents/Developpement/EnglishTest/files/anglais - adverbes.csv', LANGUE.index("EN"))
fr_words = build_words_list('/Users/alexandrelods/Documents/Developpement/EnglishTest/files/anglais - adverbes.csv', LANGUE.index("FR"))

#print( len(en_words))
#print( random.randrange(len(en_words)))
#print( random.randint(0, 1))

score = 0

for i in range(10):
	index_choice = random.randrange(len(en_words))
	languague_choix = random.randrange(2)
	if (languague_choix == LANGUE.index("EN")):
		if (type_an_answer( en_words[index_choice], LANGUE.index("EN")).lower() == fr_words[index_choice].lower()):
			print("*** Yes !")
			score = score + 1
		else:
			print("*** The answer is " + fr_words[index_choice])
	elif (languague_choix == LANGUE.index("FR")):
		if (type_an_answer( fr_words[index_choice], LANGUE.index("FR")).lower() == en_words[index_choice].lower()):
			print("*** Yes !")
			score = score + 1
		else:
			print("*** The answer is " + en_words[index_choice])
	else:
		print("[ERROR] language does not exist")

print("#### FINAL SCORE : %d / 10\n\n" % score)

# FIN -- MAIN CODE