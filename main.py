from getters import *
import csv

start = time.time()

# Nom du fichier horodaté
"""dateFile = time.strftime(getFileInfo("dateFormat"))
fileType = getFileInfo("fileType")"""

path = getFileInfo("path")
filename = "%s\%s_%s.csv" % (path, getFileInfo("genre"), time.strftime(getFileInfo("dateFormat")))

# les colonnes
section = getsection()
fieldnames = getkeys(section[0])

maxRecords = int(getFileInfo("maxRecords"))
# ouvrir le fichier csv en mode écriture
with open(filename, 'w', newline='') as csvfile:
    # créer un écrivain csv
    writer = csv.writer(csvfile, delimiter= getFileInfo("delimiteur"))
    #writer = csv.writer(csvfile)
    # écrire les en-têtes de colonne
    writer.writerow(fieldnames)
    for j in range(1, maxRecords + 1):
        writer.writerow(getData(fieldname) for fieldname in fieldnames)



end = time.time()
print("le nbr de ligne est "+ str(maxRecords)+" lignes")
print("csv généré en " + str(end - start) + " secondes")
print("csv généré en " + str((end - start)/60) + "minutes")