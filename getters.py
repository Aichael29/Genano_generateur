import random
import datetime
import time
import os
import re
from configparser import ConfigParser
from dict import DICTIONNAIRE
import sys

#TYPE, FORMAT, VALUES = 0,1,2

# le chemin absolut du fichier
absPath = os.path.dirname(os.path.realpath(__file__))
configFile = os.path.join(absPath, 'config.conf')
data = ConfigParser()
# charger le fichier de conf
data.read(configFile)

# les sections
sectionName = list(data.sections())

# les sous sections de la première section
fieldnames = list(data[sectionName[0]].keys())


#verifier les patterns du conf values à partir du dict
def regex_checker(val, dtype):
    if dtype in DICTIONNAIRE:
        regex_pattern = DICTIONNAIRE[dtype]
        pattern = re.compile(regex_pattern)
        if not pattern.match(str(val)):
            raise ValueError(f"{val} doesn't match the correspondent pattern of {dtype} in dict.py")
    else:
        raise ValueError(f"{dtype} type isn't included in dict.py")

# fonction pour obtenir les infos sur le fichier CSV
def getFileInfo(undersection):
    field = data['fileInfos'][undersection]
    return field

# convertir au type souhaité
def convertTo(dval, dtype, limit=None):
    res = []
    res = [dtype(x) for x in dval.split('-')]
    if not limit == None:
        if len(res) == limit:
            return res
        else:
            raise TypeError(f"'{dval}' is not the Length of {limit}")
            return None
    return res

# obtenir un entier aleatoire
def getRandomInt(val,form=""):
    start , end = convertTo(val, int, 2)
    return random.randint(start, end)

# float aleatoire
def getRandomFloat(val, form=""):
    start , end = convertTo(val, float, 2)
    randomFloat = lambda x,y : round(random.uniform(x, y),2)
    return randomFloat(start, end)

# string aleatoire
def getRandomString(val,form=""):
    strings = convertTo(val, str)
    return random.choice(strings)

def getRandomBoolean(val,form=""):
    strings = convertTo(val, str, 2)
    return random.choice(strings)

def date(d):
    day, month, year = d.split("/")
    sdate = datetime.date(int(year),int(month),int(day))
    # generer les timestamps
    return time.mktime(sdate.timetuple())

# retourner une date aleatoire
def getRandomDate(val,form=""):
    start , end = convertTo(val, date, 2)
    randomDate =random.randint(start, end)
    return datetime.datetime.fromtimestamp(randomDate).strftime(form)

# timestamp aleatoire
def getTimestamp(val,form=""):
    start, end = convertTo(val, date, 2)
    randomDate = random.randint(int(start), int(end))
    return datetime.datetime.fromtimestamp(randomDate).strftime(form)

currentId = 0

if 'id' in data[sectionName[0]]:
    try:
        currentId = data[sectionName[0]]['id'].split(',')[2]
        currentId = int(currentId) - 1
    except:
        sys.exit('id structure is wrong')

def getCurrentId(inData,form=""):
    global currentId
    currentId += 1
    return currentId

# les types possibles
dataTypes = {'int': getRandomInt,
             'string': getRandomString,
             'float': getRandomFloat,
             'timestamp': getTimestamp,
             "datetime": getRandomDate,
             'boolean': getRandomBoolean, # Vu que ca contient yes/no
             'id':getCurrentId,
             }

# fonction pour obtenir/generer les ranges
def getData(fieldname):
    field = data[sectionName[0]][fieldname].split(',')
    if len(field) == 3:
        dtype = field[0]
        if dtype in dataTypes:
            regex_checker(field[2], dtype)
            return dataTypes[dtype](field[2],form=field[1])
        else:
            raise TypeError(f'{dtype} is not supported')
    else:
        raise IndexError(f'{fieldname} list index out of range')
