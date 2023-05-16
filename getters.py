import random
import datetime
import time
import os
import configparser
from dict import DICTIONNAIRE
import re
import sys
import numpy as np
# le chemin absolu du fichier
absPath = os.path.dirname(os.path.realpath(__file__))
configFile = os.path.join(absPath, 'config.conf')
data = configparser.ConfigParser()
# charger le fichier de conf
data.read(configFile)
maxRecords = data["fileInfos"]["maxRecords"]

sectionName=[section for section in data.sections()]
# fonction pour obtenir les cles
def getkeys(section):
    return data[section].keys()
# fonction pour obtenir les vals des cles
def getvalues(section, key):
    return data[section][key].split(",")


# fonction pour obtenir les infos sur le fichier
def getFileInfo(undersection):
    return data['fileInfos'][undersection]

# Fonctions pour la conversion des types
def date(year):
    day, month, year_str = year.split("/")
    year_int = int(year_str)
    month_int = int(month)
    day_int = int(day)
    date_obj = datetime.date(year_int, month_int, day_int)
    timestamp = time.mktime(date_obj.timetuple())
    return timestamp


def getRandomPhone(val, form=""):
   return "".join(["+212", str(random.randint(6, 7)), str(random.randint(10000000, 99999999))])


# retourner une liste du type souhaite
def typeapproved(inData, dtype):
    valid_values = [value for value in inData.split("-") if re.search(DICTIONNAIRE[dtype], value)]
    if len(valid_values) < len(inData.split("-")):
        print("Au moins une valeur est incorrecte. Veuillez saisir des valeurs conformes au type", dtype)
    return valid_values


values = [str(i) for i in getvalues(sectionName[0], 'id_date')]
currentId = 0
sectionName=[section for section in data.sections()]

def getCurrentId(inData,form=""):
    global currentId
    currentId=int(currentId)
    if currentId == 0:
        currentId = values[2]
    else:
        currentId = currentId + 1
    return currentId




# obtenir un entier aleatoire
def getRandomInt(intSet , form=""):
    try:
        i = typeapproved(intSet, "int")
        return np.random.randint(i[0], i[1])
    except ValueError:
        raise ValueError("Valeurs invalides pour les bornes de l'intervalle")


# obtenir un double aleatoire
def getRandomFloat(intSet, form=""):
    try:
        i = typeapproved(intSet, "float")
        start = i[0]
        end = i[1]
        randomDouble = lambda x, y: random.uniform(x, y)
        return randomDouble(float(start), float(end))
    except:
        sys.exit("erreur float")

# string aleatoire
def getRandomString(intSet, form=""):
    try:
       # strings = typeapproved(intSet, "str")
        return random.choice(typeapproved(intSet, "str"))
    except:
        sys.exit("erreur str")

# retourner une date aleatoire entre 2 annees (ex: entre 2002 et 2021)
def getRandomDate(dateTime, form=""):
    try:
        i = typeapproved(dateTime, "datetime")
        start = i[0]
        end = i[1]  # date c'est une fonction
        randomDate = random.randint(int(date(start)), int(date(end)))
        return datetime.datetime.fromtimestamp(randomDate).strftime(form)
    except:
        sys.exit("erreur date")

def getTimestamp(Time, form=""):
    try:
        i = typeapproved(Time, "timestamp")
        start,end = i[0],i[1]
        randomDate = random.randint(int(date(start)), int(date(end)))  # date c'est une fonction
        return datetime.datetime.fromtimestamp(randomDate).strftime(form)
    except:
        sys.exit("erreur getTimestamp")

def getRandomBoolean(val,form=""):
    try:
        return random.choice(typeapproved(val, "bool"))
    except:
        sys.exit("erreur boolean")

def getIncrementalString(start, form=""):
    try:
        global currentId
        currentId += 1
        return start + str(currentId)
    except:
        sys.exit("erreur chaine de caractère + nombre autoincrement")

# Add the new type to the dataTypes dictionary
dataTypes = {
    'int': getRandomInt,
    'str': getRandomString,
    'timestamp': getTimestamp,
    'float': getRandomFloat,
    "datetime": getRandomDate,
    "bool": getRandomBoolean,
    "mdn": getRandomPhone,
    "autoincrement": getCurrentId,
    "chaine_autoincrement": getIncrementalString
}


def getData(fieldname):
    section = sectionName[0]
    field = getvalues(section, fieldname)
    dtype = field[0]

    # Traitement du champ 'dn'
    if fieldname == 'dn':
        type_reseau = getvalues(section, 'type_reseau')[0]
        type_destination = getvalues(section, 'type_destination')[0]

        if type_reseau == 'fix':
            field[2] = "2125" + str(random.randint(10000000, 99999999))
        else:
            field[2] = "2126" + str(random.randint(10000000, 99999999))

        if type_destination == 'international':
            field[2] = "000" + str(random.randint(100000000, 999999999))

    # Traitement du champ 'type_even'
    if fieldname == 'type_even':
        type_even = field[2]
        marche = getvalues(section, 'marche')[2]

        if type_even == 'voice' and marche == 'home':
            # Effectuer l'action souhaitée lorsque type_even est "voice" et marche est "home"
            pass

    # Traitement du champ 'even_minutes'
    if fieldname == 'even_minutes':
        type_even = getvalues(section, 'type_even')[2]

        if type_even == 'sms':
            field[2] = ''

    # Traitement du champ 'type_destination'
    if fieldname == 'type_destination':
        type_destination = field[2]

        if type_destination == 'international':
            field[2] = 'International'

    # Traitement du champ 'operator'
    if fieldname == 'operator':
        operator = field[2]
        country = getvalues(section, 'country')[2]

        if operator == 'International':
            zones = ['zone1', 'zone2', 'zone3', 'zone4']
            field[2] = random.choice(zones)

        if country != 'Morocco':
            field[2] = 'International'

    # Traitement du champ 'billing_type'
    if fieldname == 'billing_type':
        billing_type = field[2]

        if billing_type == 'prepaid':
            field[2] = 'mobile prepaid'

    # Traitement du champ 'segment'
    if fieldname == 'segment':
        segment = field[2]

        if segment == 'B2B':
            field[2] = 'prepaid'

    # Traitement du champ 'date_debut'
    if fieldname == 'date_debut':
        end = getData('date_fin')
        field[2] = getTimestamp([field[2], end], form=field[1])

    # Traitement du champ 'date_fin'
    if fieldname == 'date_fin':
        start = getData('date_debut')
        field[2] = getTimestamp([start, field[2]], form=field[1])

    if dtype in dataTypes:
        return dataTypes[dtype](field[2], form=field[1])

    return field[2]


