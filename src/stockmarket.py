# coding: utf-8

# IMPORTS

import csv
import os
import yfinance
from datetime import datetime
from forex_python.converter import CurrencyRates

# FIN -- IMPORTS



##########################################################################
# FONCTIONS UTILITAIRES A RECOPIER
##########################################################################

# RETOURNER LES NOMS DES FICHIERS D'UN REPERTOIRE PASSE EN PARAMETRE
def list_fileNames(_folder):
	files = []
	for _path, _dirs, _files in os.walk(_folder):
		for f in _files:
			files.append(f)
	return files

# MESSAGE DE DEMARRAGE DU PROGRAMME
def start_program():
	print("#############################################################")
	print("#                                                           #")
	print("#                      STOCKS LIST                          #")
	print("#                                                           #")
	print("#                  $ python3 stocks.py                      #")
	print("#############################################################")
	print()
	return datetime.now()

# MENU DE DEMARRAGE
def menu():
	print("Taper 1 pour créer un fichier listant l'ensemble des ordres effectués")
	print("Taper 2 pour créer un fichier listant l'ensemble des dividendes")
	menu = input("Votre choix : ").strip()
	print("-------------------------------------------------------------")
	return menu

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

# FIN - FONCTIONS UTILITAIRES A RECOPIER
##########################################################################




##########################################################################
# FONCTIONS PRIVEES
##########################################################################

def _convert_currencies(_from, _to, _amount, _date):
	
	currency_API = CurrencyRates()
	try:
		return round(currency_API.get_rate(_from, _to, _date) * float(_amount ), 2) if _from != _to else _amount
	except ValueError:
		print(f"[DEBUG] _from = '{_from}' & _to = '{_to}' & _date = '{_date}' & _amount = {_amount}")
		print(f"[DEBUG] fx = '{currency_API.get_rate(_from, _to, _date)}'")
		return None


# @return le nom du broker et la liste des types possibles gérés par le fichier
def _find_broker(_file):

	print(f"[INFO] Lecture du fichier '{PATH}/{_file}'")
	
	# LISTER ICI TOUTES LES ENTETES POSSIBLES DE FICHIER CSV
	FIELDNAMES_DEGIRO_V_1 = ['Date','Heure','Date de','Produit','Code ISIN','Description','FX','Mouvements','','Solde','','ID Ordre']
	FIELDNAMES_DEGIRO_V_2 = ['Date','Heure','Produit','Code ISIN','Place boursiè','Lieu d\'exécution','Quantité','Cours','Devise','Montant devise locale','','Montant','','Taux de change','Frais de courtage','','Montant négocié','','ID Ordre']
	FIELDNAMES_REVOLUT_V_1 = ['Date','Ticker','Type','Quantity','Price per share','Total Amount','Currency','FX Rate']
	FIELDNAMES_TRADING212_V_1 = ['Action','Time','ISIN','Ticker','Name','No. of shares','Price / share','Currency (Price / share)','Exchange rate','Result','Currency (Result)','Total','Currency (Total)','Notes','ID','Currency conversion fee','Currency (Currency conversion fee)']
	FIELDNAMES_TRADING212_V_2 = ['Action','Time','ISIN','Ticker','Name','No. of shares','Price / share','Currency (Price / share)','Exchange rate','Result','Currency (Result)','Total','Currency (Total)','ID','Currency conversion fee','Currency (Currency conversion fee)']
	FIELDNAMES_TRADING212_V_3 = ['Action','Time','ISIN','Ticker','Name','No. of shares','Price / share','Currency (Price / share)','Exchange rate','Result','Currency (Result)','Total','Currency (Total)','Notes','ID']

	with open(PATH + "/" + _file) as file:

		reader = csv.DictReader(file)
		
		# ALGORITHME DE RECHERCHE EN FONCTION DE L'ENTETE
		if reader.fieldnames.__eq__(FIELDNAMES_DEGIRO_V_1):
			return "DEGIRO", ["DIVIDEND"]

		if reader.fieldnames.__eq__(FIELDNAMES_DEGIRO_V_2):
			return "DEGIRO", ["STOCKS"]

		if reader.fieldnames.__eq__(FIELDNAMES_REVOLUT_V_1):
			return "REVOLUT", ["DIVIDEND", "STOCKS"]
		
		if reader.fieldnames.__eq__(FIELDNAMES_TRADING212_V_1):
			return "TRADING212", ["DIVIDEND", "STOCKS"]

		if reader.fieldnames.__eq__(FIELDNAMES_TRADING212_V_2):
			return "TRADING212", ["DIVIDEND", "STOCKS"]

		if reader.fieldnames.__eq__(FIELDNAMES_TRADING212_V_3):
			return "TRADING212", ["DIVIDEND", "STOCKS"]

	return None 


def _add_order(_file, _fieldnames,
	_date, _broker, _type, _tickerCode, _isinCode, # DATE, BROKER, "BUY" OR "SELL", TICKER, ISIN, 
	_quantity, _unitPrice, _amount, _currency, # QUANTITY, UNIT PRICE, AMOUNT, CURRENCY
	_row:str):
	
	# controler que _type est une valeur connue
	# les seules valeurs autorisées sont celles de la variable globale TYPES
	if len([x for x in TYPES if str(x) == _type]) == 0:
		print(f"[ERROR] ligne échappée {_row} RAISON = _type (valeur = '{_type}') n'est pas géré ")
		return False # sort de la méthode
	
	# controler que _quantity est un nombre positif ou nul
	try:
		float(_quantity)
	except ValueError:
		print(f"[ERROR] ligne échappée {_row} RAISON = _quantity (valeur = '{_quantity}') n'est pas convertible en float,")
		return False # sort de la méthode
	
	if (float(_quantity) < 0):
		print(f"[ERROR] ligne échappée {_row} RAISON = _quantity (valeur = '{_quantity}') devrait être positif ou égal à 0,")
		return False # sort de la méthode
		
	# controler que _date est une date
	# @TODO


	# controler que _unitPrice est un nombre positif ou nul
	try:
		float(_unitPrice)
	except ValueError:
		print(f"[ERROR] ligne échappée {_row} RAISON = _unitPrice (valeur = '{_unitPrice}') n'est pas convertible en float,")
		return False # sort de la méthode
	
	if (float(_unitPrice) < 0):
		print(f"[ERROR] ligne échappée {_row} RAISON = _unitPrice (valeur = '{_unitPrice}') devrait être positif ou égal à 0,")
		return False # sort de la méthode
		
	# controler que _amount est un nombre positif ou nul
	try:
		float(_amount)
	except ValueError:
		print(f"[ERROR] ligne échappée {_row} RAISON = _amount (valeur = '{_amount}') n'est pas convertible en float,")
		return False # sort de la méthode
	
	if (float(_amount) < 0):
		print(f"[ERROR] ligne échappée {_row} RAISON = _amount (valeur = '{_amount}') devrait être positif ou égal à 0,")
		return False # sort de la méthode

	# on crée une ligne dans le fichier csv
	row = {
			"DATE": _date.strftime("%d/%m/%Y"),
			"BROKER": _broker,
			"TYPE": _type,
			"TICKER": _tickerCode,
			"ISIN": _isinCode,
			"QUANTITY": _quantity,
			"UNIT PRICE": _unitPrice,
			"AMOUNT": _amount,
			"CURRENCY": _currency,
		}
	# print(f"[DEBUG] row = {row}")
	
	writer = csv.DictWriter(_file, fieldnames=_fieldnames)
	writer.writerow(row)

	return True


def _add_dividend(_file, _fieldnames,
	_date, _broker, _type, _tickerCode, _isinCode, 	# DATE, BROKER, "DIVIDEND" OR "TAX", TICKER, ISIN, 
	_amount, _currency):							# AMOUNT, CURRENCY

	# controler que _type est une valeur connue
	# les seules valeurs autorisées sont celles de la variable globale TYPES
	if len([x for x in TYPES if str(x) == _type]) == 0:
		print(f"[ERROR] le paramètre _type n'est pas géré par l'application (valeur = '{_type}' pour {_broker})")
		return False # sort de la méthode
	
	# on crée une ligne dans le fichier csv
	row = {
			"DATE": _date.strftime("%d/%m/%Y"),
			"BROKER": _broker,
			"TYPE": _type,
			"TICKER": _tickerCode,
			"ISIN": _isinCode,
			"AMOUNT": _amount,
			"CURRENCY": _currency,
		}
	
	writer = csv.DictWriter(_file, fieldnames=_fieldnames)
	writer.writerow(row)

	return True


# FIN - FONCTIONS PRIVEES
##########################################################################



##########################################################################
# FONCTIONS EXPOSABLES
##########################################################################

# lister l'ensemble des ordres de bourse
# dans le fichier CSV fourni en paramètre _outcome
def list_all_stockMarketOrder(_outcome):
	
	FIELDNAMES = [
		'DATE', 
		'BROKER', 
		'TYPE', 
		'TICKER', 
		'ISIN', 
		'QUANTITY', 
		'UNIT PRICE', 
		'AMOUNT', 
		'CURRENCY'
		]
	
	# initialisation du fichier de résultat
	writer = csv.DictWriter(_outcome, fieldnames=FIELDNAMES)
	writer.writeheader()

	# pour chaque fichier .csv trouvé dans le répertoire PATH
	for f in [x for x in list_fileNames(PATH) if str(x).endswith('.csv')] :
		
		print(f"[INFO] Lecture du fichier '{PATH}/{f}'")
		
		with open(PATH + "/" + f) as file:
			reader = csv.DictReader(file)

			# recherche du broker
			brocker_to_uppercase = str(f).upper().split(" ")[0] # TODO revoir la recherche de brocker à l'aide de REGEX
			
			# pour chaque ligne du fichier csv
			for row in reader:
				
				# TODO streamer row dans une base de données BIG DATA

				match brocker_to_uppercase:
					
					case "DEGIRO":
						date = datetime.strptime(row["Date"] + " " + row["Heure"], "%d-%m-%Y %H:%M")
						type = "BUY" if float(row["Montant"]) < 0 else "SELL" 	# value = <value_if_true> if <expression> else <value_if_false>
						isin = row["Code ISIN"]
						ticker = "NA"
						quantity = abs(float(row["Quantité"]))
						price = row["Cours"]
						amount = str(row["Montant devise locale"]).replace(",", "").replace("-","")
						currency = row["Devise"]
							
					case "TRADING212":
						# mapping du type d'opération
						match str(row["Action"]).upper(): 
								case "MARKET BUY": 
									type = TYPES[0] 
									quantity = row["No. of shares"].replace(",", "").replace("-","")
									price = row["Price / share"].replace(",", "").replace("-","")
									amount = round(float(quantity)*float(price),2)
								case "MARKET SELL": 
									type = TYPES[1]
									quantity = row["No. of shares"].replace(",", "").replace("-","")
									price = row["Price / share"].replace(",", "").replace("-","")
									amount = round(float(quantity)*float(price),2)
								case _: 
									type = row["Action"]
									quantity = 0
									price = ""
									amount = ""

						date = datetime.strptime(row["Time"], "%Y-%m-%d %H:%M:%S")
						ticker = row["Ticker"]
						isin = row["ISIN"]
						currency = row["Currency (Price / share)"]
							
					case "REVOLUT":
						# mapping du type d'opération
						match str(row["Type"]).upper(): 
								case "BUY - MARKET": 
									type = TYPES[0] 
									quantity = row["Quantity"]
								case "SELL - MARKET": 
									type = TYPES[1]
									quantity = row["Quantity"]
								case _: 
									type = row["Type"]
									quantity = 0
						
						# convertir la date
						# REVOLUT donne une date précise avec hh:mm:ss au format iso
						date = datetime.fromisoformat(row["Date"])
						
						# prix unitaire
						price = str(row["Price per share"])[1:].replace(",", "").replace("-","")
						amount = str(row["Total Amount"])[1:].replace(",", "").replace("-","")

						# trouver l'isin à partir du ticker
						isin = "TBD" if len(row["Ticker"]) > 0 else "TBD" # value = <value_if_true> if <expression> else <value_if_false>
						
						ticker = row["Ticker"]
						currency = row["Currency"]
							
					case "BOURSORAMA":
						print(f"[ERROR] Broker '{brocker_to_uppercase}' non géré")
						print(f"[ERROR] développement en attente de la mise à disposition d'une extraction complète par '{brocker_to_uppercase}'")
						break

					case _:
						print(f"[ERROR] Broker '{brocker_to_uppercase}' non géré")
						print(f"[ERROR] Revoir le nom du fichier")
						print(f"[ERROR] ou ajouter le broker au programme stocks.py")
						break

				# ajoute à _outcome les données présentes dans chaque fichier du broker
				_add_order(
					_outcome, 
					FIELDNAMES, 
					date, 
					brocker_to_uppercase, 
					type, 
					ticker, 
					isin, 
					quantity, 
					price, 
					amount, 
					currency, 
					row.__str__()
					)
	
	# Sortie OK lorsque toutes les lignes ont été insérées
	return True


# lister l'ensemble des dividendes
# dans le fichier CSV @param _outcome
def list_all_dividend(_outcome):

	FIELDNAMES = [
		'DATE', 
		'BROKER', 
		'TYPE', 
		'TICKER', 
		'ISIN', 
		'AMOUNT', 
		'CURRENCY'
		]
	
	# initialisation du fichier de résultat
	writer = csv.DictWriter(_outcome, fieldnames=FIELDNAMES)
	writer.writeheader()

	# pour chaque fichier .csv trouvé dans le répertoire PATH
	for f in [x for x in list_fileNames(PATH) if str(x).endswith('.csv')] :
		
		print(f"[INFO] Lecture du fichier '{PATH}/{f}'")
		
		with open(PATH + "/" + f) as file:
			reader = csv.DictReader(file)

			# recherche du broker
			brocker_to_uppercase = str(f).upper().split(" ")[0]
			# print(f"[DEBUG] broker = '{brocker_to_uppercase}'")

			# TODO revoir la recherche de brocker à l'aide de REGEX

			match brocker_to_uppercase:
				
				case "DEGIRO":
					
					# pour chaque ligne du fichier du broker
					for row in reader:

						# mapping du type d'opération
						match str(row["Description"]).upper().split(): 
								case "DIVIDENDE": 
									type = TYPES[2] 
								case "IMPOTS SUR DIVIDENDE": 
									type = TYPES[3]
								case _: 
									type = row["Description"]

						# ajoute à _outcome les données présentes dans chaque fichier du broker
						_add_dividend(
							_outcome, 																# _file
							FIELDNAMES,
							datetime.strptime(row["Date"] + " " + row["Heure"], "%d-%m-%Y %H:%M"), 	# _date
							brocker_to_uppercase, 													# _broker
							type,																	# _type
							"NA", 																	# _tickerCode
							row["Code ISIN"], 														# _isinCode
							row[""], 
							row["Mouvements"], 
						)
				case _:
					print(f"[ERROR] Broker '{brocker_to_uppercase}' non géré")
					print(f"[ERROR] Revoir le nom du fichier")
					print(f"[ERROR] ou ajouter le broker au programme stocks.py")

	return True

# FIN - FONCTIONS EXPOSABLES
##########################################################################


############ MAIN #############
def main():
	
	start = start_program()
	print()
	print(f"Mettre les fichiers de vos différents brokers dans {PATH}")
	print()

	match menu():
		case "1": # LISTER TOUTES LES OPERATIONS ACHAT / VENTE DE TITRE
			print()
			print(f"Le résultat sera disponible dans {PATH}/allstockmarket-orders.csv")
			print()
			print("-------------------------------------------------------------")
			print()
			list_all_stockMarketOrder(open(PATH + "/allstockmarket-orders.csv", "w"))

		case "2": # LISTER LES DIVIDENDES VERSES & LES IMPOTS DEJA PRELEVES
			print()
			print(f"Le résultat sera disponible dans {PATH}/allstockmarket-dividend.csv")
			print()
			print("-------------------------------------------------------------")
			print()
			list_all_dividend(open(PATH + "/allstockmarket-dividend.csv", "w"))

		case "test_yfinance()":
			msft = yfinance.Ticker("MSFT")
			print("isin = " + msft.get_isin())
			print(msft.get_dividends())
			print(msft.get_info())

		case "_find_broker()":
			print()
			print(f"Parcourir le répertoire {PATH}")
			print()
			print("-------------------------------------------------------------")
			# pour chaque fichier .csv trouvé dans le répertoire PATH
			for f in [x for x in list_fileNames(PATH) if str(x).endswith('.csv')] :
				print(_find_broker(f))

		case _:
			print("[ERROR] Choix non implémenté")

	finish = end_program()
	print_executionTime(start, finish)
############ FIN - MAIN #############

if __name__ == "__main__":
	PATH = "/Users/alexandrelods/Documents/Developpement/PythonCode/files/stocks"
	TYPES = ["BUY", "SELL", "DIVIDEND", "TAX"]
	main()