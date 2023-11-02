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


BROKERS_DATA_PATH = "/Users/alexandrelods/Documents/Developpement/PythonCode/data/stocks"

ORDER_TYPES = ["BUY", "SELL"]
DIVIDEND_TYPES = ["DIVIDEND", "TAX"]
ALL_TYPES = ORDER_TYPES + DIVIDEND_TYPES

STOCKS_ORDERS_HEADER = [
            "DATE",
            "BROKER",
            "TYPE",
            "TICKER",
            "ISIN",
            "QUANTITY",
            "UNIT PRICE",
            "AMOUNT",
            "CURRENCY",
        ]

DEFAULT_VALUE = "TBD"
MS_API_ACCESS_KEY = "89497626879422c72731d9e603dac6a8"

##########################################################################
# FONCTIONS UTILITAIRES A RECOPIER
##########################################################################

#  💣  💥  🔥  📛  ⛔  ❌  🚫  ❗  ✅
#  🚧  🚨  💬
#  🌩  🌧  🌥
#  ⏰  
#  📁  📄  📝  🔎
#  🔜  ⇢

def list_fileNames(_folder) -> list:
    """ 
    Retourne une liste de nom de fichier présent dans le répertoire passé en paramètre\n

    Args:
        _folder (str) : directory or folder

    Returns:
        list of filenames (list of str)
    """

    files = []
    for _path, _dirs, _files in os.walk(_folder):
        for f in _files:
            files.append(_path + "/" + f)
    return files


def start_program() -> datetime:
    """ 
    Message de démarrage du programme, renvoie l'heure exacte de démarrage du programme\n
    
    Returns:
        datime.now()
    """

    print()
    print("🚀 stocks.py")
    print()
    return datetime.now()


# MENU DE DEMARRAGE
def menu() -> str:
    """ 
    Affiche un menu de sélection\n
    
    Returns:
        the user's prompt
    """

    print("1️⃣   pour créer un fichier listant l'ensemble des ordres effectués")
    print(
        "2️⃣   pour créer un fichier listant l'ensemble des ordres effectués et classés par ordre chronologique"
    )
    print("3️⃣   pour donner la répartition de son portefeuille")
    print("4️⃣   pour créer un fichier listant l'ensemble des dividendes")
    print()
    menu = input("⇢ Votre choix : ").strip()
    return menu


# MESSAGE DE FIN DU PROGRAMME
def end_program() -> datetime:
    """ 
    Message de fin du programme, renvoie l'heure exacte de fin du programme\n
    
    Returns:
        datime.now()
    """

    print()
    print()
    return datetime.now()


# TEMPS D'EXECUTION DU PROGRAMME
def print_executionTime(_start, _finish) -> datetime:
    """ 
    Mesure le temps écoulé entre deux dates et l'affiche en console\n

    Args:
        _start (datetime) : 1st date of the interval
        _finish (datetime) : 2nd date of the interval

    Returns:
        difference between ``_finish`` and ``_start``
    """

    print(f"⏰ {_finish - _start}")
    print()
    return _finish - _start


# FIN - FONCTIONS UTILITAIRES A RECOPIER
##########################################################################


##########################################################################
# FONCTIONS PRIVEES
##########################################################################


def _convert_currencies(_from, _to, _amount, _date) -> float:
    """ 
    Converti une somme exprimée en monnaie ``_from`` vers la monnaire ``_to`` au taux de conversion valable à la date ``_date``\n
    
    Args:
        _from (str) : initial currency
        _to (str) : final currency
        _date (datetime) : a date of the conversion
        _amount (str, int or float) : amount to convert

    Returns:
        amount (float) or None if currency does not exist
    """

    currency_API = CurrencyRates()
    try:
        return (
            round(currency_API.get_rate(_from, _to, _date) * float(_amount), 2)
            if _from != _to
            else float(_amount)
        )
    except ValueError:
        print("💥 in _convert_currencies() method")
        print(
            f"  _from = '{_from}' & _to = '{_to}' & _date = '{_date}' & _amount = {_amount}"
        )
        return None


# @return le code isin à partir du ticker
# TODO revoir le contenu du fichier .csv
def _find_isin(_ticker, _currency):
    FIELDNAMES = ["symbol", "isin", "currency", "name", "region", "region_code"]

    with open(BROKERS_DATA_PATH + "/database isin ticker.csv") as file:
        reader = csv.DictReader(file, fieldnames=FIELDNAMES, delimiter=";")
        for row in reader:
            if row["symbol"] == _ticker and row["currency"] == _currency:
                return row["isin"]

    return None


# @return le code isin à partir du ticker
# TODO revoir le contenu du fichier .csv
def _find_ticker(_isin, _currency):
    FIELDNAMES = ["symbol", "isin", "currency", "name", "region", "region_code"]

    with open(BROKERS_DATA_PATH + "/database isin ticker.csv") as file:
        reader = csv.DictReader(file, fieldnames=FIELDNAMES, delimiter=";")
        for row in reader:
            if row["isin"] == _isin and row["currency"] == _currency:
                return row["symbol"]

    return _isin


def _find_broker(_file) -> tuple:
    """ 
    Détermine le broker utilisé pour générer le fichier des ordres de bourse\n
    
    Args:
        _file (str) : file name

    Returns:
        a tuple with the broker name and the list of possible operations
    """

    # LISTER ICI TOUTES LES ENTETES POSSIBLES DE FICHIER CSV
    FIELDNAMES_DEGIRO_V_1 = [
        "Date",
        "Heure",
        "Date de",
        "Produit",
        "Code ISIN",
        "Description",
        "FX",
        "Mouvements",
        "",
        "Solde",
        "",
        "ID Ordre",
    ]
    FIELDNAMES_DEGIRO_V_2 = [
        "Date",
        "Heure",
        "Produit",
        "Code ISIN",
        "Place boursiè",
        "Lieu d'exécution",
        "Quantité",
        "Cours",
        "",
        "Montant devise locale",
        "",
        "Montant",
        "",
        "Taux de change",
        "Frais de courtage",
        "",
        "Montant négocié",
        "",
        "ID Ordre",
    ]
    FIELDNAMES_REVOLUT_V_1 = [
        "Date",
        "Ticker",
        "Type",
        "Quantity",
        "Price per share",
        "Total Amount",
        "Currency",
        "FX Rate",
    ]
    FIELDNAMES_TRADING212_V_1 = [
        "Action",
        "Time",
        "ISIN",
        "Ticker",
        "Name",
        "No. of shares",
        "Price / share",
        "Currency (Price / share)",
        "Exchange rate",
        "Result",
        "Currency (Result)",
        "Total",
        "Currency (Total)",
        "Notes",
        "ID",
        "Currency conversion fee",
        "Currency (Currency conversion fee)",
    ]
    FIELDNAMES_TRADING212_V_2 = [
        "Action",
        "Time",
        "ISIN",
        "Ticker",
        "Name",
        "No. of shares",
        "Price / share",
        "Currency (Price / share)",
        "Exchange rate",
        "Result",
        "Currency (Result)",
        "Total",
        "Currency (Total)",
        "ID",
        "Currency conversion fee",
        "Currency (Currency conversion fee)",
    ]
    FIELDNAMES_TRADING212_V_3 = [
        "Action",
        "Time",
        "ISIN",
        "Ticker",
        "Name",
        "No. of shares",
        "Price / share",
        "Currency (Price / share)",
        "Exchange rate",
        "Result",
        "Currency (Result)",
        "Total",
        "Currency (Total)",
        "Notes",
        "ID",
    ]

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

# @TODO retirer la référence à _file et _fieldnames puisque ces deniers sont fixés par le programme lui même
def _add_order(
    _outcome : csv.DictWriter,
    _date: datetime,
    _broker: str,
    _type: str,
    _tickerCode: str,
    _isinCode: str,
    _quantity: float,
    _unitPrice: float,
    _amount: float,
    _currency: str,
    _row: str,
):
    """ 
    Ajoute dans le fichier .CSV ``_outcome`` un ordre de bourse caractérisé par sa date d'exécution, son montant,
    sa référence isin, sa référence de ticker, le sens d'opération (vente ou achat),
    la quantité échangée, le prix unitaire et la monnaie de l'instrument financier\n
    
    Args:
        _outcome (DictWriter) : csv file
        _date (datetime) : execution date
        _broker (str) : broker's name
        _type (str) : one value in ["BUY", "SELL"]
        _tickerCode (str) : ticker code
        _isinCode (str) : isin code
        _quantity (float) : quantity
        _unitPrice (float) : unit price
        _amount (float, optional) : should be equals to ``_quantity`` * ``_unitPrice``
        _currency (str) : currency iso code (ex: EUR, USD, ...)
        _row (str, optional) : original line in the broker's file

    Returns:
        True if market order is correctly added in ``_file``, False if not
    """
    
    # le controle que _date est une date est effectué 
    # par python lui-meme en ayant précisé ``: datetime`` en description de la fonction

    # controler que _type est une valeur connue
    # parmi les seules valeurs autorisées
    # i.e. celles de la variable globale ORDER_TYPES
    if len([x for x in ORDER_TYPES if str(x) == _type]) == 0:
        #print(f"🚧 ligne échappée {_row} RAISON = _type (valeur = '{_type}') n'est pas géré ")
        return False # sort de la méthode

    # controler que _quantity est un nombre positif ou nul
    try:
        float(_quantity)
    except ValueError:
        print(
            f"⛔ ligne échappée {_row} RAISON = _quantity (valeur = '{_quantity}') n'est pas convertible en float,"
        )
        return False  # sort de la méthode

    if float(_quantity) < 0:
        print(
            f"⛔ ligne échappée {_row} RAISON = _quantity (valeur = '{_quantity}') devrait être positif ou égal à 0,"
        )
        return False  # sort de la méthode

    # controler que _unitPrice est un nombre positif ou nul
    try:
        float(_unitPrice)
    except ValueError:
        print(
            f"⛔ ligne échappée {_row} RAISON = _unitPrice (valeur = '{_unitPrice}') n'est pas convertible en float,"
        )
        return False  # sort de la méthode

    if float(_unitPrice) < 0:
        print(
            f"⛔ ligne échappée {_row} RAISON = _unitPrice (valeur = '{_unitPrice}') devrait être positif ou égal à 0,"
        )
        return False  # sort de la méthode

    # controler que _amount est un nombre positif ou nul
    try:
        float(_amount)
    except ValueError:
        print(
            f"⛔ ligne échappée {_row} RAISON = _amount (valeur = '{_amount}') n'est pas convertible en float,"
        )
        return False  # sort de la méthode

    if float(_amount) < 0:
        print(
            f"⛔ ligne échappée {_row} RAISON = _amount (valeur = '{_amount}') devrait être positif ou égal à 0,"
        )
        return False  # sort de la méthode

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

    _outcome.writerow(row)

    return True

# @TODO retirer la référence à _file et _fieldnames puisque ces deniers sont fixés par le programme lui même
def _add_dividend(
    _file,
    _fieldnames,
    _date: datetime,
    _broker: str,
    _type: str,
    _tickerCode: str,
    _isinCode: str,
    _amount: float,
    _currency: str,
):
    """ 
    Ajoute dans le fichier .CSV ``_file`` un dividende caractérisé par sa date de perception, son montant,
    sa référence isin, sa référence de ticker, la monnaie du dividende perçu\n
    
    Args:
        _file (str) : csv file name
        _fieldnames (list) : à retirer
        _date (datetime) : execution date
        _broker (str) : broker's name
        _type (str) : one value in ["DIVIDEND", "TAX"]
        _tickerCode (str) : ticker code
        _isinCode (str) : isin code
        _amount (float) : dividend's amount
        _currency (str) : currency iso code (ex: EUR, USD, ...)

    Returns:
        True if market order is correctly added in ``_file``, False if not
    """

    # controler que _type est une valeur connue
    # les seules valeurs autorisées sont celles de la variable globale TYPES
    if len([x for x in ALL_TYPES if str(x) == _type]) == 0:
        print(
            f"🚧 le paramètre _type n'est pas géré par l'application (valeur = '{_type}' pour {_broker})"
        )
        return False  # sort de la méthode

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
    
    writer = csv.DictWriter(_outcome, fieldnames=STOCKS_ORDERS_HEADER)
    writer.writeheader()

    # pour chaque fichier .csv trouvé dans le répertoire PATH
    for f in [x for x in list_fileNames(BROKERS_DATA_PATH) if str(x).endswith(".csv")]:
        print()
        print(f"📄 Lecture du fichier '{f}'")

        with open(f) as file:
            reader = csv.DictReader(file)

            # recherche du broker
            brocker = _find_broker(str(f))

            # si le fichier du brocker n'est pas compatible avec la fonctionnalité
            if not brocker[1] or not "_add_order" in brocker[1]:
                print(f"❌ le fichier n'est pas compatible avec la fonctionnalité ``market orders``")
                continue
            else :
                print(f"✅ le fichier est  compatible avec la fonctionnalité ``market orders``")

            # pour chaque ligne du fichier csv
            for row in reader:
                # TODO streamer row dans une base de données BIG DATA

                match brocker[0]:
                    case "DEGIRO":
                        date = datetime.strptime(
                            row["Date"] + " " + row["Heure"], "%d-%m-%Y %H:%M"
                        )
                        type = (
                            "BUY" if float(row["Montant"]) < 0 else "SELL"
                        )  # value = <value_if_true> if <expression> else <value_if_false>
                        isin = row["Code ISIN"]
                        quantity = abs(float(row["Quantité"]))
                        amount = (
                            str(row["Montant"])
                            .replace(",", "")
                            .replace("-", "")
                        )
                        price = round(float(amount) / quantity,2)
                        currency = row[""]  # TODO smelly code puisque DEGIRO spécifie des noms de colonnes vides  --> "EUR"
                        ticker = _find_isin(isin, currency)

                    case "TRADING 212":
                        # mapping du type d'opération
                        match str(row["Action"]).upper():
                            case "MARKET BUY":
                                type = ALL_TYPES[0]
                                quantity = (
                                    row["No. of shares"]
                                    .replace(",", "")
                                    .replace("-", "")
                                )
                                price = (
                                    row["Price / share"]
                                    .replace(",", "")
                                    .replace("-", "")
                                )
                                amount = round(float(quantity) * float(price), 2)
                            case "MARKET SELL":
                                type = ALL_TYPES[1]
                                quantity = (
                                    row["No. of shares"]
                                    .replace(",", "")
                                    .replace("-", "")
                                )
                                price = (
                                    row["Price / share"]
                                    .replace(",", "")
                                    .replace("-", "")
                                )
                                amount = round(float(quantity) * float(price), 2)
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
                                type = ALL_TYPES[0]
                                quantity = row["Quantity"]
                            case "SELL - MARKET":
                                type = ALL_TYPES[1]
                                quantity = row["Quantity"]
                            case _:
                                type = row["Type"]
                                quantity = 0

                        date = datetime.fromisoformat(row["Date"])
                        price = (
                            str(row["Price per share"])[1:]
                            .replace(",", "")
                            .replace("-", "")
                        )
                        amount = (
                            str(row["Total Amount"])[1:]
                            .replace(",", "")
                            .replace("-", "")
                        )
                        ticker = row["Ticker"]
                        currency = row["Currency"]
                        isin = _find_isin(ticker, currency)

                    case _:
                        print(f"🚧 Broker '{brocker}' non géré")
                        print(f"  Revoir le nom du fichier")
                        print(f"  ou ajouter le broker au programme stocks.py")
                        break

                # ajoute à _outcome les données présentes dans chaque fichier du broker
                _add_order(
                    writer,
                    date,
                    brocker[0],
                    type,
                    ticker,
                    isin,
                    quantity,
                    price,
                    amount,
                    currency,
                    row.__str__(),
                )
    
    # Sortie OK lorsque toutes les lignes ont été insérées
    return True


def list_all_stockMarket_order_sorted(_outcome):
    assets = []

    FIELDNAMES = [
        "DATE",
        "BROKER",
        "TYPE",
        "TICKER",
        "ISIN",
        "QUANTITY",
        "UNIT PRICE",
        "AMOUNT",
        "CURRENCY",
    ]

    # pour chaque fichier .csv trouvé dans le répertoire PATH
    for f in [x for x in list_fileNames(BROKERS_DATA_PATH) if str(x).endswith(".csv")]:
        print(f"📄 Lecture du fichier '{f}'")

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
                                type = ALL_TYPES[0]
                                quantity = row["Quantity"]
                            case "SELL - MARKET":
                                type = ALL_TYPES[1]
                                quantity = row["Quantity"]
                            case _:
                                type = row["Type"]
                                quantity = 0

                        # convertir la date
                        # REVOLUT donne une date précise avec hh:mm:ss au format iso
                        date = datetime.fromisoformat(row["Date"])
                        price = (
                            str(row["Price per share"])[1:]
                            .replace(",", "")
                            .replace("-", "")
                        )
                        amount = (
                            str(row["Total Amount"])[1:]
                            .replace(",", "")
                            .replace("-", "")
                        )
                        ticker = row["Ticker"]
                        currency = row["Currency"]
                        isin = _find_isin(ticker, currency)

                    case "DEGIRO":
                        date = datetime.strptime(
                            row["Date"] + " " + row["Heure"], "%d-%m-%Y %H:%M"
                        )
                        type = (
                            "BUY" if float(row["Montant"]) < 0 else "SELL"
                        )  # value = <value_if_true> if <expression> else <value_if_false>
                        isin = row["Code ISIN"]
                        quantity = abs(float(row["Quantité"]))
                        price = row["Cours"]
                        amount = (
                            str(row["Montant devise locale"])
                            .replace(",", "")
                            .replace("-", "")
                        )
                        currency = row[
                            ""
                        ]  # TODO smelly code due to DEGIRO  with several empty fieldnames
                        ticker = _find_ticker(isin, currency)

                    case "TRADING 212":
                        # mapping du type d'opération
                        match str(row["Action"]).upper():
                            case "MARKET BUY":
                                type = ALL_TYPES[0]
                                quantity = (
                                    row["No. of shares"]
                                    .replace(",", "")
                                    .replace("-", "")
                                )
                                price = (
                                    row["Price / share"]
                                    .replace(",", "")
                                    .replace("-", "")
                                )
                                amount = round(float(quantity) * float(price), 2)

                            case "MARKET SELL":
                                type = ALL_TYPES[1]
                                quantity = (
                                    row["No. of shares"]
                                    .replace(",", "")
                                    .replace("-", "")
                                )
                                price = (
                                    row["Price / share"]
                                    .replace(",", "")
                                    .replace("-", "")
                                )
                                amount = round(float(quantity) * float(price), 2)

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
                        print(f"🚧 Broker '{brocker}' non géré")
                        print(f"  Revoir le nom du fichier")
                        print(f"  ou ajouter le broker au programme stocks.py")
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
                assets.append(
                    (
                        date,
                        brocker[0],
                        type,
                        ticker,
                        isin,
                        quantity,
                        price,
                        amount,
                        currency,
                    )
                )

    print(assets)

    # initialisation du fichier de résultat
    writer = csv.DictWriter(_outcome, fieldnames=FIELDNAMES)
    writer.writeheader()

    for asset in sorted(assets, key=lambda asset: asset[0].isoformat()):
        _add_order(
            _outcome,
            FIELDNAMES,
            asset[0],
            asset[1],
            asset[2],
            asset[3],
            asset[4],
            asset[5],
            asset[6],
            asset[7],
            asset[8],
            str(asset),
        )

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
        "DATE",  # TODO mettre la date en notation américaine
        "BROKER",
        "TYPE",
        "TICKER",
        "ISIN",
        "AMOUNT",
        "CURRENCY",
    ]

    # initialisation du fichier de résultat
    writer = csv.DictWriter(_outcome, fieldnames=FIELDNAMES)
    writer.writeheader()

    # pour chaque fichier .csv trouvé dans le répertoire PATH
    for f in [x for x in list_fileNames(BROKERS_DATA_PATH) if str(x).endswith(".csv")]:
        print(f"📄 Lecture du fichier '{f}'")

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
                                type = ALL_TYPES[2]
                            case "IMPOTS SUR DIVIDENDE":
                                type = ALL_TYPES[3]
                            case _:
                                type = row["Description"]

                        # ajoute à _outcome les données présentes dans chaque fichier du broker
                        _add_dividend(
                            _outcome,  # _file
                            FIELDNAMES,
                            datetime.strptime(
                                row["Date"] + " " + row["Heure"], "%d-%m-%Y %H:%M"
                            ),  # _date
                            brocker_to_uppercase,  # _broker
                            type,  # _type
                            "NA",  # _tickerCode
                            row["Code ISIN"],  # _isinCode
                            row[""],
                            row["Mouvements"],
                        )
                case _:
                    print(f"🚧 Broker '{brocker_to_uppercase}' non géré")
                    print(f"  Revoir le nom du fichier")
                    print(f"  ou ajouter le broker au programme stocks.py")

    return True


def get_stockMarket_portfolio(_input, _output):
    FIELDNAMES = ["BROKER", "TICKER", "ISIN", "QUANTITY", "UNIT PRICE", "CURRENCY"]

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
                    "unit price": (q1 * p1 + q2 * p2) / (q1 + q2)
                    if q1 + q2 != 0
                    else 0,
                    "currency": row["CURRENCY"],
                    "isin": row["ISIN"],
                    "broker": row["BROKER"]
                }
            elif row["TYPE"] == "SELL":
                asset_value = {
                    "quantity": q1 - q2,
                    "unit price": (q1 * p1 - q2 * p2) / (q1 - q2)
                    if q1 - q2 != 0
                    else 0,
                    "currency": row["CURRENCY"],
                    "isin": row["ISIN"],
                    "broker": row["BROKER"]
                }
            else:
                continue

        else:
            if row["TYPE"] == "BUY":
                asset_value = {
                    "quantity": row["QUANTITY"],
                    "unit price": row["UNIT PRICE"],
                    "currency": row["CURRENCY"],
                    "isin": row["ISIN"],
                    "broker": row["BROKER"]
                }
            elif row["TYPE"] == "SELL":
                asset_value = {
                    "quantity": "-" + row["QUANTITY"],
                    "unit price": "-" + row["UNIT PRICE"],
                    "currency": row["CURRENCY"],
                    "isin": row["ISIN"],
                    "broker": row["BROKER"]
                }
            else:
                continue

        assets[row["TICKER"]] = asset_value

    writer = csv.DictWriter(_output, fieldnames=FIELDNAMES)
    writer.writeheader()

    for asset in sorted(assets) :
        row = {
            "BROKER": assets[asset]["broker"],
            "TICKER": asset,
            "ISIN": assets[asset]["isin"],
            "QUANTITY": assets[asset]["quantity"],
            "UNIT PRICE": assets[asset]["unit price"],
            "CURRENCY": assets[asset]["currency"],
        }

        if float(row["QUANTITY"]) > float(
            "1e-003"
        ):  # permet de filtrer les lignes donc la quantité est inférieure à 0.001
            # ce qui peut arriver à cause des arrondis
            writer.writerow(row)

    return assets


# FIN - FONCTIONS EXPOSABLES
##########################################################################


############ MAIN #############
def main():
    start = start_program()
    print(f"\U0001F4C1 {BROKERS_DATA_PATH}")
    print()

    match menu():
        case "1":  # LISTER TOUTES LES OPERATIONS ACHAT / VENTE DE TITRE
            print()
            print(f"🔜 Le résultat sera disponible dans {BROKERS_DATA_PATH}/all stockmarket orders.csv")
            print()
            print()
            list_all_stockMarket_order(open(BROKERS_DATA_PATH + "/all stockmarket orders.csv", "w"))

        case "2":  # LISTER ET CLASSER TOUTES LES OPERATIONS ACHAT / VENTE DE TITRE
            print()
            print(
                f"🔜 Le résultat sera disponible dans {BROKERS_DATA_PATH}/all stockmarket orders (sorted).csv"
            )
            print()
            print()
            list_all_stockMarket_order_sorted(
                open(BROKERS_DATA_PATH + "/all stockmarket orders (sorted).csv", "w")
            )

        case "3":  # DONNER LA COMPOSITION D'UN PORTEFEUILLE
            print()
            print(f"🔜 Le résultat sera disponible dans {BROKERS_DATA_PATH}/portfolio.csv")
            print()
            print()
            list_all_stockMarket_order_sorted(
                open(BROKERS_DATA_PATH + "/all stockmarket orders (sorted).csv", "w")
            )
            assets = get_stockMarket_portfolio(
                open(BROKERS_DATA_PATH + "/all stockmarket orders (sorted).csv", "r"),
                open(BROKERS_DATA_PATH + "/portfolio.csv", "w"),
            )

        case "4":  # LISTER LES DIVIDENDES VERSES & LES IMPOTS DEJA PRELEVES
            print()
            print(
                f"🔜 Le résultat sera disponible dans {BROKERS_DATA_PATH}/all stockmarket dividend.csv"
            )
            print()
            print()
            list_all_stockMarket_dividend(
                open(BROKERS_DATA_PATH + "/all stockmarket dividend.csv", "w")
            )

        case "_find_broker":
            print()
            print(f"📁 {BROKERS_DATA_PATH}")
            print()
            # pour chaque fichier .csv trouvé dans le répertoire PATH
            for f in [x for x in list_fileNames(BROKERS_DATA_PATH) if str(x).endswith(".csv")]:
                print(_find_broker(f))

		# sandbox
		# scenario à venir
        case "_yfinance":
            msft = yfinance.Ticker("CNDX")
            print("isin = " + msft.get_isin())
            print(msft.get_dividends())
            print(msft.get_info())

        case "_ms":
            url = (
                "http://api.marketstack.com/v1/tickers/MSFT"
                + "?access_key="
                + MS_API_ACCESS_KEY
            )
            api_response = requests.get(url)
            print(api_response.status_code)
            api_json = (
                api_response.json() if api_response != None else None
            )  # api_json = api_response.json() if api_response and api_response.status_code == 200 else None
            print()
            print(api_json)
			
        case _:
            # print()
            print("❌ ce choix n'existe pas")

    finish = end_program()
    print_executionTime(start, finish)


############ FIN - MAIN #############

if __name__ == "__main__":
    main()
