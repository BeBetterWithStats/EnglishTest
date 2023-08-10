# coding: utf-8

# IMPORTS

import csv
import os
import yfinance
from datetime import datetime
from forex_python.converter import CurrencyRates

# FIN -- IMPORTS



##########################################################################
# FONCTION UTILITAIRE A RECOPIER
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

##########################################################################


def _convert_currencies(_from, _to, _amount, _date):
	
	currency_API = CurrencyRates()
	try:
		return round(currency_API.get_rate(_from, _to, _date) * float(_amount ), 2) if _from != _to else _amount
	except ValueError:
		print(f"[DEBUG] _from = '{_from}' & _to = '{_to}' & _date = '{_date}' & _amount = {_amount}")
		print(f"[DEBUG] fx = '{currency_API.get_rate(_from, _to, _date)}'")
		return None

def _find_broker(_file):

	print(f"[INFO] Lecture du fichier '{PATH}/{_file}'")
	
	FIELDNAMES_DEGIRO_ACCOUNT = ['Date','Heure','Date de','Produit','Code ISIN','Description','FX','Mouvements','','Solde','','ID Ordre']
	FIELDNAMES_DEGIRO_TRANSACTIONS = ['Date','Heure','Produit','Code ISIN','Place boursiè','Lieu d\'exécution','Quantité','Cours','Devise','Montant devise locale','','Montant','','Taux de change','Frais de courtage','','Montant négocié','','ID Ordre']
	FIELDNAMES_REVOLUT = ['Date','Ticker','Type','Quantity','Price per share','Total Amount','Currency','FX Rate']
	FIELDNAMES_TRADING212_VERSION1 = ['Action','Time','ISIN','Ticker','Name','No. of shares','Price / share','Currency (Price / share)','Exchange rate','Result','Currency (Result)','Total','Currency (Total)','Notes','ID','Currency conversion fee','Currency (Currency conversion fee)']
	FIELDNAMES_TRADING212_VERSION2 = ['Action','Time','ISIN','Ticker','Name','No. of shares','Price / share','Currency (Price / share)','Exchange rate','Result','Currency (Result)','Total','Currency (Total)','ID','Currency conversion fee','Currency (Currency conversion fee)']
	FIELDNAMES_TRADING212_VERSION3 = ['Action','Time','ISIN','Ticker','Name','No. of shares','Price / share','Currency (Price / share)','Exchange rate','Result','Currency (Result)','Total','Currency (Total)','Notes','ID']

	with open(PATH + "/" + _file) as file:

		reader = csv.DictReader(file)
		
		if reader.fieldnames.__eq__(FIELDNAMES_DEGIRO_ACCOUNT):
			return "DEGIRO", "DIVIDEND"

		if reader.fieldnames.__eq__(FIELDNAMES_DEGIRO_TRANSACTIONS):
			return "DEGIRO", "STOCKS"

		if reader.fieldnames.__eq__(FIELDNAMES_REVOLUT):
			return "REVOLUT", ""
		
		if reader.fieldnames.__eq__(FIELDNAMES_TRADING212_VERSION1):
			return "TRADING212", ""

		if reader.fieldnames.__eq__(FIELDNAMES_TRADING212_VERSION2):
			return "TRADING212", ""

		if reader.fieldnames.__eq__(FIELDNAMES_TRADING212_VERSION3):
			return "TRADING212", ""

	print(reader.fieldnames)
	return None 

def _add_stockMarketOrder(_file, _fieldnames,
	_date, _broker, _type, _tickerCode, _isinCode, 	# DATE, BROKER, "BUY" OR "SELL", TICKER, ISIN, 
	_quantity, _unitPrice, _amount, _currency):		# QUANTITY, UNIT PRICE, AMOUNT, CURRENCY
	
	# controler que _type est une valeur connue
	# les seules valeurs autorisées sont celles de la variable globale TYPES
	if len([x for x in ORDERS if str(x) == _type]) == 0:
		print(f"[ERROR] le paramètre _type n'est pas géré par l'application (valeur = '{_type}' pour {_broker})")
		return False # sort de la méthode
	
	# controler que _quantity est un nombre positif ou nul
	try:
		float(_quantity)
		if (float(_quantity) < 0):
			print(f"[ERROR] le paramètre _quantity devrait être positif ou égal à 0, ce n'est pas le cas pour {_broker} ")
			return False # sort de la méthode
		
	except ValueError:
		print(f"[ERROR] le paramètre _quantity n'est pas convertible en float (valeur = '{_quantity}' pour {_broker})")
		return False # sort de la méthode
	
	# controler que _date est une date
	# @TODO


	# controler que _unitPrice est un nombre positif ou nul
	try:
		float(_unitPrice)
		if (float(_unitPrice) < 0):
			print(f"[ERROR] le paramètre _unitPrice devrait être positif ou égal à 0, ce n'est pas le cas pour {_broker} ")
			return False # sort de la méthode
		
	except ValueError:
		print(f"[ERROR] le paramètre _unitPrice n'est pas convertible en float (valeur = '{_unitPrice}' pour {_broker})")
		return False # sort de la méthode
	
	# controler que _amount est un nombre positif ou nul
	try:
		float(_amount)
		if (float(_amount) < 0):
			print(f"[ERROR] le paramètre _amount devrait être positif ou égal à 0, ce n'est pas le cas pour {_broker} ")
			return False # sort de la méthode
		
	except ValueError:
		print(f"[ERROR] le paramètre _amount n'est pas convertible en float (valeur = '{_amount}' pour {_broker})")
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

# lister l'ensemble des ordres de bourse
# dans le fichier CSV @param _outcome
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
			brocker_to_uppercase = str(f).upper().split(" ")[0]
			# TODO revoir la recherche de brocker à l'aide de REGEX

			match brocker_to_uppercase:
				
				case "DEGIRO":

					# pour chaque ligne du fichier du broker
					for row in reader:

						# ajoute à _outcome les données présentes dans chaque fichier du broker
						_add_stockMarketOrder(
							_outcome, 																# _file
							FIELDNAMES,
							datetime.strptime(row["Date"] + " " + row["Heure"], "%d-%m-%Y %H:%M"), 	# _date
							brocker_to_uppercase, 													# _broker
							"BUY" if float(row["Montant"]) < 0 else "SELL",							# _buyOrSell
																									#      value = <value_if_true> if <expression> else <value_if_false>
							"NA", 																	# _tickerCode
							row["Code ISIN"], 														# _isinCode
							abs(float(row["Quantité"])),											# _quantity
							row["Cours"],															# _unitPrice
							str(row["Montant devise locale"]).replace(",", "").replace("-",""),		# _amount
							row["Devise"]															# _currency
							)
						
				case "TRADING212":
					
					# pour chaque ligne du fichier du broker
					for row in reader:

						# mapping du type d'opération
						match str(row["Action"]).upper(): 
								case "MARKET BUY": 
									type = ORDERS[0] 
									quantity = row["No. of shares"].replace(",", "").replace("-","")
									price = row["Price / share"].replace(",", "").replace("-","")
									amount = round(float(quantity)*float(price),2)
								case "MARKET SELL": 
									type = ORDERS[1]
									quantity = row["No. of shares"].replace(",", "").replace("-","")
									price = row["Price / share"].replace(",", "").replace("-","")
									amount = round(float(quantity)*float(price),2)
								case _: 
									type = row["Action"]
									quantity = 0
									price = ""
									amount = ""

						# ajoute à _outcome les données présentes dans chaque fichier du broker
						_add_stockMarketOrder(
							_outcome, 																# _file
							FIELDNAMES,
							datetime.strptime(row["Time"], "%Y-%m-%d %H:%M:%S"), 					# _date
							brocker_to_uppercase, 													# _broker
							type,																	# _buyOrSell
							row["Ticker"], 															# _tickerCode
							row["ISIN"], 															# _isinCode
							quantity,																# _quantity
							price,																	# _unitPrice
							amount,																	# _amount
							row["Currency (Price / share)"]											# _currency
							)
					
				case "REVOLUT":

					# pour chaque ligne du fichier du broker
					for row in reader:
							
						# mapping du type d'opération
						match str(row["Type"]).upper(): 
								case "BUY - MARKET": 
									type = ORDERS[0] 
									quantity = row["Quantity"]
								case "SELL - MARKET": 
									type = ORDERS[1]
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
						
						# ajoute à _outcome les données présentes dans chaque fichier du broker
						_add_stockMarketOrder(
							_outcome, 															# _file
							FIELDNAMES,
							date,																# _date
							brocker_to_uppercase, 												# _broker
							type,																# _buyOrSell
							row["Ticker"], 														# _tickerCode
							"NA",																# _isinCode
							quantity,															# _quantity
							price,																# _unitPrice
							amount,																# _amount
							row["Currency"],													# _currency
							)
						
				case "BOURSORAMA":
					print(f"[ERROR] Broker '{brocker_to_uppercase}' non géré")
					print(f"[ERROR] développement en attente de la mise à disposition d'une extraction complète par '{brocker_to_uppercase}'")

				case _:
					print(f"[ERROR] Broker '{brocker_to_uppercase}' non géré")
					print(f"[ERROR] Revoir le nom du fichier")
					print(f"[ERROR] ou ajouter le broker au programme stocks.py")


	return True

def _add_dividend(_file, _fieldnames,
	_date, _broker, _type, _tickerCode, _isinCode, 	# DATE, BROKER, "DIVIDEND" OR "TAX", TICKER, ISIN, 
	_amount, _currency):							# AMOUNT, CURRENCY

	# controler que _type est une valeur connue
	# les seules valeurs autorisées sont celles de la variable globale TYPES
	if len([x for x in ORDERS if str(x) == _type]) == 0:
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
									type = ORDERS[2] 
								case "IMPOTS SUR DIVIDENDE": 
									type = ORDERS[3]
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



def main():
	
	start = start_program()
	print()
	print(f"Mettre les fichiers de vos différents brokers dans {PATH}")
	print()

	match menu():
		case "1":
			print()
			print(f"Le résultat sera disponible dans {PATH}/allstockmarket-orders.csv")
			print()
			print("-------------------------------------------------------------")
			print()
			list_all_stockMarketOrder(open(PATH + "/allstockmarket-orders.csv", "w"))

		case "2":
			print()
			print(f"Le résultat sera disponible dans {PATH}/allstockmarket-dividend.csv")
			print()
			print("-------------------------------------------------------------")
			print()
			list_all_dividend(open(PATH + "/allstockmarket-dividend.csv", "w"))

		case "test_yfinance":
			msft = yfinance.Ticker("MSFT")
			print("isin = " + msft.get_isin())
			print(msft.get_dividends())
			print(msft.get_info())

		case "test_find_broker":
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




# MAIN CODE
if __name__ == "__main__":

	PATH = "/Users/alexandrelods/Documents/Developpement/PythonCode/files/stocks"
	ORDERS = ["BUY", "SELL", "DIVIDEND", "TAX"]

	main()


