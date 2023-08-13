# coding: utf-8

# IMPORTS

import os
import re
from pytube import YouTube
from sys import argv
from datetime import date
from datetime import datetime

# FIN -- IMPORTS

##########################################################################
# FONCTION UTILITAIRE A RECOPIER
##########################################################################

# RETOURNER LES NOMS DES FICHIERS D'UN REPERTOIRE PASSE EN PARAMETRE
def list_fileNames(_folder):
	files = []
	for _path, _dirs, _files in os.walk(_folder):
		for _file in _files:
			files.append(_file)
	return files

# MESSAGE DE DEMARRAGE DU PROGRAMME
def start_program():
	print("#############################################################")
	print("#                                                           #")
	print("#                  YOUTUBE DOWNLOADER                       #")
	print("#                                                           #")
	print("#     $ python3 youtube-downloader.py <URL youtube>         #")
	print("#                                                           #")
	print("#############################################################")
	print()
	return datetime.now()

# MESSAGE DE FIN DU PROGRAMME
def end_program():
	print()
	print("#############################################################")
	return datetime.now()

# TEMPS D'EXECUTION DU PROGRAMME
def print_executionTime(_start, _finish):
	print()
	print(f"[INFO] execution = {_finish - _start}")
	print()

##########################################################################

def _is_urlValide(_url):
	# https://youtu.be/MLu3I8tjKEg
	# https://www.youtube.com/live/I4eVdFPjVgA?feature=share
	condition = re.search(r"^(https|http):\/\/[www.]*youtu[a-zA-Z0-9_.=?-]+", _url)
	# condition = re.search(r"^(https|http):\/\/[a-zA-Z0-9.]*youtu[a-zA-Z0-9_.=?-]+", _url)
	return True if condition else False

############ MAIN #############
def main():
	PATH = "/Users/alexandrelods/Downloads/youtube_dl"

	start = start_program()


	if len(argv) != 2:
		link = input("Quelle est l'URL de la vidéo youtube à télécharger ? ").strip()
	else :
		link = argv[1].strip

	# TODO ajouter un controle de l'url avec une REGEX
	# https://youtu.be/MLu3I8tjKEg
	# https://www.youtube.com/live/I4eVdFPjVgA?feature=share
	if not _is_urlValide(link):
		return print(f"[ERROR] le lien de téléchargement '{link}' n'est pas valide")


	print(f"[INFO] Téléchargement de la vidéo '{link}'")

	yt = YouTube(link)
	print("[INFO] Titre = '" + yt.title + "'")
	print("[INFO] Auteur = '" + yt.author + "'")

	yt.streams.get_highest_resolution().download(PATH)
	print(f"[INFO] Vidéo disponible dans le répertoire '{PATH}'")

	end = end_program()
	print_executionTime(start, end)

	return True
############ FIN - MAIN #############


if __name__ == "__main__":

	link = input("Quelle est l'URL de la vidéo youtube à télécharger ? ").strip()
	print(_is_urlValide(link))
	# main()