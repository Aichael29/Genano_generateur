from getters import *
import csv
import time
import multiprocessing
# les colonnes
section = sectionName
fieldnames = getkeys(section[0])
maxRecords = int(getFileInfo("maxRecords"))
num_processes = multiprocessing.cpu_count()
# Fonction qui génère les données pour une plage donnée
def generate_data(start, end, fieldnames):
    data = []
    for j in range(start, end):
        data.append([getData(fieldname) for fieldname in fieldnames])
    return data

if __name__ == '__main__':
    start = time.time()

    # Nom du fichier horodaté
    path = getFileInfo("path")
    filename = "%s\%s_%s.csv" % (path, getFileInfo("genre"), time.strftime(getFileInfo("dateFormat")))



    # diviser le travail en plusieurs tranches
    slice_size = maxRecords // num_processes
    slices = [(i * slice_size, (i + 1) * slice_size) for i in range(num_processes)]
    if maxRecords % num_processes != 0:
        slices.append((num_processes * slice_size, maxRecords))

    # utiliser multiprocessing pour générer les données en parallèle
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = []
        for s in slices:
            results.append(pool.apply_async(generate_data, args=(s[0]+1, s[1]+1, fieldnames)))
        data = []
        for r in results:
            data += r.get()

    # ouvrir le fichier csv en mode écriture
    with open(filename, 'w', newline='') as csvfile:
        # créer un écrivain csv
        writer = csv.writer(csvfile, delimiter=getFileInfo("delimiter"))

        # écrire les en-têtes de colonne
        writer.writerow(fieldnames)

        # écrire les données générées
        for row in data:
            writer.writerow(row)

    end = time.time()
    print("le nbr de ligne est "+ str(maxRecords)+" lignes")
    print("csv généré en " + str(end - start) + " secondes")
