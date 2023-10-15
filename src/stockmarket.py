# coding: utf-8

# IMPORTS

import csv
import os
import yfinance
import requests
import json
from datetime import datetime
from forex_python.converter import CurrencyRates

# FIN -- IMPORTS


PATH = "/Users/alexandrelods/Documents/Developpement/PythonCode/data/stocks"
TYPES = ["BUY", "SELL", "DIVIDEND", "TAX"]
DEFAULT_VALUE = "TBD"
MS_API_ACCESS_KEY = "89497626879422c72731d9e603dac6a8"

##########################################################################
# FONCTIONS UTILITAIRES A RECOPIER
##########################################################################

# RETOURNER LES NOMS DES FICHIERS D'UN REPERTOIRE PASSE EN PARAMETRE
def list_fileNames(_folder):
	files = []
	for _path, _dirs, _files in os.walk(_folder):
		for f in _files:
			files.append(_path + "/" + f)
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
	print("Taper 2 pour créer un fichier listant l'ensemble des ordres effectués et classés par ordre chronologique")
	print("Taper 3 pour donner la répartition de son portefeuille")
	print("Taper 4 pour créer un fichier listant l'ensemble des dividendes")
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

# @return _amount converti de la monnaie _from vers la monnaire _to au taux de conversion valable à la date _date
def _convert_currencies(_from, _to, _amount, _date):
	
	currency_API = CurrencyRates()
	try:
		return round(currency_API.get_rate(_from, _to, _date) * float(_amount ), 2) if _from != _to else _amount
	except ValueError:
		print(f"[DEBUG] _from = '{_from}' & _to = '{_to}' & _date = '{_date}' & _amount = {_amount}")
		print(f"[DEBUG] fx = '{currency_API.get_rate(_from, _to, _date)}'")
		return None

# @return le code isin à partir du ticker
def _find_isin(_ticker, _currency):

	FIELDNAMES = [
		'symbol', 
		'isin', 
		'currency', 
		'name', 
		'region', 
		'region_code'
		]
	
	with open(PATH + "/database isin ticker.csv") as file:

		reader = csv.DictReader(file, fieldnames=FIELDNAMES, delimiter=";")
		for row in reader:
			if (row["symbol"] == _ticker and row["currency"] == _currency):
				return row["isin"]
			
	return None

# @return le code isin à partir du ticker
def _find_ticker(_isin, _currency):

	FIELDNAMES = [
		'symbol', 
		'isin', 
		'currency', 
		'name', 
		'region', 
		'region_code'
		]
	
	with open(PATH + "/database isin ticker.csv") as file:

		reader = csv.DictReader(file, fieldnames=FIELDNAMES, delimiter=";")
		for row in reader:
			if (row["isin"] == _isin and row["currency"] == _currency):
				return row["symbol"]
			
	return None

# @return le nom du broker et la liste des types possibles gérés par le fichier
def _find_broker(_file):

	# LISTER ICI TOUTES LES ENTETES POSSIBLES DE FICHIER CSV
	FIELDNAMES_DEGIRO_V_1 = ['Date','Heure','Date de','Produit','Code ISIN','Description','FX','Mouvements','','Solde','','ID Ordre']
	FIELDNAMES_DEGIRO_V_2 = ['Date','Heure','Produit','Code ISIN','Place boursiè','Lieu d\'exécution','Quantité','Cours','','Montant devise locale','','Montant','','Taux de change','Frais de courtage','','Montant négocié','','ID Ordre']
	FIELDNAMES_REVOLUT_V_1 = ['Date','Ticker','Type','Quantity','Price per share','Total Amount','Currency','FX Rate']
	FIELDNAMES_TRADING212_V_1 = ['Action','Time','ISIN','Ticker','Name','No. of shares','Price / share','Currency (Price / share)','Exchange rate','Result','Currency (Result)','Total','Currency (Total)','Notes','ID','Currency conversion fee','Currency (Currency conversion fee)']
	FIELDNAMES_TRADING212_V_2 = ['Action','Time','ISIN','Ticker','Name','No. of shares','Price / share','Currency (Price / share)','Exchange rate','Result','Currency (Result)','Total','Currency (Total)','ID','Currency conversion fee','Currency (Currency conversion fee)']
	FIELDNAMES_TRADING212_V_3 = ['Action','Time','ISIN','Ticker','Name','No. of shares','Price / share','Currency (Price / share)','Exchange rate','Result','Currency (Result)','Total','Currency (Total)','Notes','ID']

	with open(_file) as file:

		reader = csv.DictReader(file)

		if not reader.fieldnames:
			return "", None

		# ALGORITHME DE RECHERCHE EN FONCTION DE L'ENTETE
		if reader.fieldnames.__eq__(FIELDNAMES_DEGIRO_V_1):
			return "DEGIRO", ["_add_dividend"]

		if reader.fieldnames.__eq__(FIELDNAMES_DEGIRO_V_2):
			return "DEGIRO", ["_add_order"]

		if reader.fieldnames.__eq__(FIELDNAMES_REVOLUT_V_1):
			return "REVOLUT", ["_add_dividend", "_add_order"]
		
		if reader.fieldnames.__eq__(FIELDNAMES_TRADING212_V_1):
			return "TRADING 212", ["_add_dividend", "_add_order"]

		if reader.fieldnames.__eq__(FIELDNAMES_TRADING212_V_2):
			return "TRADING 212", ["_add_dividend", "_add_order"]

		if reader.fieldnames.__eq__(FIELDNAMES_TRADING212_V_3):
			return "TRADING 212", ["_add_dividend", "_add_order"]

	return "", None


def _add_order(_file, _fieldnames,
	_date : datetime, _broker : str, _type : str, _tickerCode : str, _isinCode : str, # DATE, BROKER, "BUY" OR "SELL", TICKER, ISIN, 
	_quantity : float, _unitPrice : float, _amount : float, _currency : str, # QUANTITY, UNIT PRICE, AMOUNT, CURRENCY
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
			"DATE": _date.strftime("%Y/%m/%d"),
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
	_date : datetime, _broker : str, _type : str, _tickerCode : str, _isinCode : str, 	# DATE, BROKER, "DIVIDEND" OR "TAX", TICKER, ISIN, 
	_amount : float, _currency : str):							# AMOUNT, CURRENCY

	# controler que _type est une valeur connue
	# les seules valeurs autorisées sont celles de la variable globale TYPES
	if len([x for x in TYPES if str(x) == _type]) == 0:
		print(f"[ERROR] le paramètre _type n'est pas géré par l'application (valeur = '{_type}' pour {_broker})")
		return False # sort de la méthode
	
	# on crée une ligne dans le fichier csv
	row = {
			"DATE": _date.strftime("%Y/%m/%d"),
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
def list_all_stockMarket_order(_outcome):
	
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
		
		print(f"[INFO] Lecture du fichier '{f}'")
		
		with open(f) as file:
			reader = csv.DictReader(file)

			# recherche du broker
			brocker = _find_broker(str(f))

			# si le fichier du brocker n'est pas compatible avec la fonctionnalité
			if not brocker[1] or not "_add_order" in brocker[1]:
				continue

			# pour chaque ligne du fichier csv
			for row in reader:
				
				# TODO streamer row dans une base de données BIG DATA

				match brocker[0]:
					
					case "DEGIRO":
						date = datetime.strptime(row["Date"] + " " + row["Heure"], "%d-%m-%Y %H:%M")
						type = "BUY" if float(row["Montant"]) < 0 else "SELL" 	# value = <value_if_true> if <expression> else <value_if_false>
						isin = row["Code ISIN"]
						quantity = abs(float(row["Quantité"]))
						price = row["Cours"]
						amount = str(row["Montant devise locale"]).replace(",", "").replace("-","")
						currency = row[""] #TODO smelly code due to DEGIRO  with several empty fieldnames
						ticker = _find_ticker(isin, currency)
						
					case "TRADING 212":
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
						
						date = datetime.fromisoformat(row["Date"])
						price = str(row["Price per share"])[1:].replace(",", "").replace("-","")
						amount = str(row["Total Amount"])[1:].replace(",", "").replace("-","")
						ticker = row["Ticker"]
						currency = row["Currency"]
						isin = _find_isin(ticker, currency)
							
					case _:
						print(f"[ERROR] Broker '{brocker}' non géré")
						print(f"[ERROR] Revoir le nom du fichier")
						print(f"[ERROR] ou ajouter le broker au programme stocks.py")
						break

				# ajoute à _outcome les données présentes dans chaque fichier du broker
				_add_order(
					_outcome, 
					FIELDNAMES, 
					date, 
					brocker[0], 
					type, 
					ticker, 
					isin, 
					quantity, 
					price, 
					amount, 
					currency, 
					row.__str__()
					)
	# TODO trier le fichier

	# Sortie OK lorsque toutes les lignes ont été insérées
	return True

def list_all_stockMarket_order_sorted(_outcome):

	assets = []

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
	

	# pour chaque fichier .csv trouvé dans le répertoire PATH
	for f in [x for x in list_fileNames(PATH) if str(x).endswith('.csv')] :
		
		print(f"[INFO] Lecture du fichier '{f}'")
		
		with open(f) as file:
			reader = csv.DictReader(file)

			# recherche du broker
			brocker = _find_broker(str(f))

			# si le fichier du brocker n'est pas compatible avec la fonctionnalité
			if not brocker[1] or not "_add_order" in brocker[1]:
				continue

			# pour chaque ligne du fichier csv
			for row in reader:
				
				# TODO streamer row dans une base de données BIG DATA

				match brocker[0]:
					
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
						price = str(row["Price per share"])[1:].replace(",", "").replace("-","")
						amount = str(row["Total Amount"])[1:].replace(",", "").replace("-","")
						ticker = row["Ticker"]
						currency = row["Currency"]
						isin = _find_isin(ticker, currency)
						
					
					case "DEGIRO":
						date = datetime.strptime(row["Date"] + " " + row["Heure"], "%d-%m-%Y %H:%M")
						type = "BUY" if float(row["Montant"]) < 0 else "SELL" 	# value = <value_if_true> if <expression> else <value_if_false>
						isin = row["Code ISIN"]
						quantity = abs(float(row["Quantité"]))
						price = row["Cours"]
						amount = str(row["Montant devise locale"]).replace(",", "").replace("-","")
						currency = row[""] #TODO smelly code due to DEGIRO  with several empty fieldnames
						ticker = _find_ticker(isin, currency)
						
					case "TRADING 212":
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
						
					case _:
						print(f"[ERROR] Broker '{brocker}' non géré")
						print(f"[ERROR] Revoir le nom du fichier")
						print(f"[ERROR] ou ajouter le broker au programme stocks.py")
						break
				
				# assets.append(
				# 				{
				# 					'DATE': date, 
				# 					'BROKER' : brocker[0], 
				# 					'TYPE': type, 
				# 					'TICKER': ticker, 
				# 					'ISIN': isin, 
				# 					'QUANTITY': quantity, 
				# 					'UNIT PRICE': price, 
				# 					'AMOUNT': amount, 
				# 					'CURRENCY': currency
				# 				}
				# 			)
				assets.append((date, brocker[0], type, ticker, isin, quantity, price, amount, currency))

	print(assets)

	# initialisation du fichier de résultat
	writer = csv.DictWriter(_outcome, fieldnames=FIELDNAMES)
	writer.writeheader()

	for asset in sorted(assets, key=lambda asset: asset[0].isoformat()):

		_add_order(_outcome, FIELDNAMES, asset[0], asset[1], asset[2], asset[3], asset[4], asset[5], asset[6], asset[7], asset[8], str(asset))
		
		# row = {
		# 	"DATE": asset[0].strftime("%Y/%m/%d"),
		# 	"BROKER": asset[1],
		# 	"TYPE": asset[2],
		# 	"TICKER": asset[3],
		# 	"ISIN": asset[4],
		# 	"QUANTITY": asset[5],
		# 	"UNIT PRICE": asset[6],
		# 	"AMOUNT": asset[7],
		# 	"CURRENCY": asset[8],
		# }
		# writer.writerow(row)

	return True


# lister l'ensemble des dividendes
# dans le fichier CSV @param _outcome
def list_all_stockMarket_dividend(_outcome):

	FIELDNAMES = [
		'DATE',  # TODO mettre la date en notation américaine
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
		
		print(f"[INFO] Lecture du fichier '{f}'")
		
		with open(f) as file:
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


def get_stockMarket_portfolio(_input, _output):

	FIELDNAMES = [
		'BROKER', 
		'TICKER', 
		'ISIN', 
		'QUANTITY', 
		'UNIT PRICE', 
		'CURRENCY'
		]
	
	assets = {}
	
	# initialisation du fichier de résultat
	reader = csv.DictReader(_input)

	for row in reader:
		if row["TICKER"] in assets:
			q1 = float(assets[row["TICKER"]]["quantity"])
			q2 = float(row["QUANTITY"])
			p1 = float(assets[row["TICKER"]]["unit price"])
			p2 = float(row["UNIT PRICE"])
			
			if row["TYPE"] == "BUY":
				asset_value = {
				"quantity": q1 + q2,
				"unit price": (q1*p1 + q2*p2)/(q1 + q2) if q1 + q2 != 0 else 0,
				"currency": row["CURRENCY"]
				}
			elif row["TYPE"] == "SELL":
				asset_value = {
				"quantity": q1 - q2,
				"unit price": (q1*p1 - q2*p2)/(q1 - q2) if q1 - q2 != 0 else 0,
				"currency": row["CURRENCY"]
				}
			else:
				continue

		else:
			if row["TYPE"] == "BUY":
				asset_value = {
					"quantity": row["QUANTITY"],
					"unit price": row["UNIT PRICE"],
					"currency": row["CURRENCY"]
				}
			elif row["TYPE"] == "SELL":
				asset_value = {
					"quantity": "-" + row["QUANTITY"],
					"unit price": "-" + row["UNIT PRICE"],
					"currency": row["CURRENCY"]
				}
			else:
				continue
	
		assets[row["TICKER"]] = asset_value

	writer = csv.DictWriter(_output, fieldnames=FIELDNAMES)
	writer.writeheader()

	for asset in assets:

		row = {
			"BROKER": "",
			"TICKER": asset,
			"ISIN": "",
			"QUANTITY": assets[asset]["quantity"],
			"UNIT PRICE": assets[asset]["unit price"],
			"CURRENCY": assets[asset]["currency"]
		}
		
		if float(row["QUANTITY"]) > float('1e-003') : # permet de filtrer les lignes donc la quantité est inférieure à 0.001
													  # ce qui peut arriver à cause des arrondis
			writer.writerow(row)

	return assets

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
			print(f"Le résultat sera disponible dans {PATH}/all stockmarket orders.csv")
			print()
			print("-------------------------------------------------------------")
			print()
			list_all_stockMarket_order(open(PATH + "/all stockmarket orders.csv", "w"))

		case "2": # LISTER ET CLASSER TOUTES LES OPERATIONS ACHAT / VENTE DE TITRE
			print()
			print(f"Le résultat sera disponible dans {PATH}/all stockmarket orders (sorted).csv")
			print()
			print("-------------------------------------------------------------")
			print()
			list_all_stockMarket_order_sorted(open(PATH + "/all stockmarket orders (sorted).csv", "w"))

		case "3": # DONNER LA COMPOSITION D'UN PORTEFEUILLE
			print()
			print(f"Le résultat sera disponible dans {PATH}/portfolio.csv")
			print()
			print("-------------------------------------------------------------")
			print()
			list_all_stockMarket_order_sorted(open(PATH + "/all stockmarket orders (sorted).csv", "w"))
			assets = get_stockMarket_portfolio(
												open(PATH + "/all stockmarket orders (sorted).csv", "r"),
												open(PATH + "/portfolio.csv", "w"))
		
		case "4": # LISTER LES DIVIDENDES VERSES & LES IMPOTS DEJA PRELEVES
			print()
			print(f"Le résultat sera disponible dans {PATH}/all stockmarket dividend.csv")
			print()
			print("-------------------------------------------------------------")
			print()
			list_all_stockMarket_dividend(open(PATH + "/all stockmarket dividend.csv", "w"))

		case "_yfinance":
			msft = yfinance.Ticker("CNDX")
			print("isin = " + msft.get_isin())
			print(msft.get_dividends())
			print(msft.get_info())

		case "_ms":
			url = "http://api.marketstack.com/v1/tickers/MSFT" + "?access_key=" + MS_API_ACCESS_KEY
			api_response = requests.get(url)
			print(api_response.status_code)
			api_json = api_response.json() if api_response != None else None # api_json = api_response.json() if api_response and api_response.status_code == 200 else None
			print()
			print(api_json)
			
		case "_find_broker":
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
	main()