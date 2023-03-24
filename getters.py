import random
import datetime
import time
import os
import configparser
from dict import DICTIONNAIRE
import re
import sys

# le chemin absolu du fichier
absPath = os.path.dirname(os.path.realpath(__file__))
configFile = os.path.join(absPath, 'config.conf')
data = configparser.ConfigParser()
# charger le fichier de conf
data.read(configFile)
maxRecords = data["fileInfos"]["maxRecords"]

# fonction pour obtenir les cles
def getkeys(section):
    return list(data[section].keys())

# fonction pour obtenir les vals des cles
def getvalues(section, key):
    return data[section][key].split(",")

# fonction pour obtenir les sections
def getsection():
    return [section for section in data.sections()]

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

def getRandomPhone(val,form=""):
    ph_no = []
    # the first number should be in the range of 6 to 7
    ph_no.append("+212")
    ph_no.append(random.randint(6, 7))
    # the for loop is used to append the other 9 numbers.
    # the other 9 numbers can be in the range of 0 to 9.
    for i in range(1,9):
        ph_no.append(random.randint(0, 9))

    return ''.join(str(e) for e in ph_no)


# retourner une liste du type souhaite
def typeapproved(inData, dtype):
    regex = DICTIONNAIRE[dtype]
    values = inData.split("-")
    valid_values = [value for value in values if re.search(regex, value)]
    if len(valid_values) < len(values):
        print("Au moins une valeur est incorrecte. Veuillez saisir des valeurs conformes au type", dtype)
    return valid_values


currentId = 0
sectionName=getsection()
if 'autoicrement' in data[sectionName[0]]:
    try:
        currentId = data[sectionName[0]]['autoicrement'].split(',')[2]
        currentId = int(currentId) - 1
    except:
        sys.exit('autoicrement structure is wrong')

def getCurrentId(inData,form=""):
    global currentId
    currentId += 1
    return currentId

# obtenir un entier aleatoire
def getRandomInt(intSet, form=""):
    try:
        i=typeapproved(intSet,"int")
        start=i[0]
        end=i[1]
        return random.randint(int(start), int(end))
    except:
        sys.exit("erreur int")

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
        strings = typeapproved(intSet, "str")
        return random.choice(strings)
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

# les types possibles
dataTypes = {
    'int': getRandomInt,
    'str': getRandomString,
    'timestamp': getTimestamp,
    'float': getRandomFloat,
    "datetime": getRandomDate,
    "bool":getRandomBoolean,
    "mdn":getRandomPhone,
    "autoicrement":getCurrentId
}

# fonction pour obtenir/generer les ranges
def getData(fieldname):
    section=getsection()
    field = getvalues(section[0], fieldname)
    dtype = field[0]
    if dtype in dataTypes:
        return dataTypes[dtype](field[2], form=field[1])
    return field[2]