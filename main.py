from getters import *
import csv
import concurrent.futures
import time

start = time.time()

# Nom du fichier horodaté
path = getFileInfo("path")
filename = "%s\%s_%s.csv" % (path, getFileInfo("genre"), time.strftime(getFileInfo("dateFormat")))

# les colonnes
section = sectionName
fieldnames = getkeys(section[0])

maxRecords = int(getFileInfo("maxRecords"))

# ouvrir le fichier csv en mode écriture
with open(filename, 'w', newline='') as csvfile:
    # créer un écrivain csv
    writer = csv.writer(csvfile,delimiter=getFileInfo("delimiter"))

    # écrire les en-têtes de colonne
    writer.writerow(fieldnames)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for j in range(1, maxRecords + 1):
            # utiliser executor pour exécuter getData() en parallèle
            row = executor.map(getData, fieldnames)
            writer.writerow(row)

end = time.time()
print("le nbr de ligne est "+ str(maxRecords)+" lignes")
print("csv généré en " + str(end - start) + " secondes")