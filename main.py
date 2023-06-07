import csv
import time
from getters import *
from multiprocessing import Pool
import multiprocessing
def generate_row(fieldnames):
    return [getData(fieldname) for fieldname in fieldnames]

if __name__ == '__main__':
    start = time.time()

    # Nom du fichier horodaté
    path = getFileInfo("path")
    filename = "%s\%s_%s.csv" % (path, getFileInfo("genre"), time.strftime(getFileInfo("dateFormat")))

    # les colonnes
    fieldnames = getkeys(sectionName[0])
    maxRecords = int(getFileInfo("maxRecords"))

    # ouvrir le fichier csv en mode écriture
    with open(filename, 'w', newline='') as csvfile:
        # créer un écrivain csv
        writer = csv.writer(csvfile, delimiter=getFileInfo("delimiter"))
        # écrire les en-têtes de colonne
        writer.writerow(fieldnames)
        num_processes = multiprocessing.cpu_count()
        # Create a multiprocessing pool with the number of desired processes
        pool = Pool(processes=num_processes)  # You can adjust the number of processes as needed

        # Generate rows using multiprocessing and write them to the CSV file
        results = pool.map(generate_row, [fieldnames] * maxRecords)
        writer.writerows(results)

    end = time.time()
    print("le nbr de ligne est " + str(maxRecords) + " lignes")
    print("csv généré en " + str(end - start) + " secondes")
