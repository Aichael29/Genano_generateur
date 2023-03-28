from getters import getFileInfo, getkeys, getData, sectionName, time
import csv
import threading

star = time.time()
# Fonction pour écrire les données dans le fichier csv
def write_data(start, end, writer):
    for i in range(start, end):
        writer.writerow(getData(fieldname) for fieldname in fieldnames)

# Récupérer le nombre de threads à utiliser en fonction du nombre de lignes de données
maxRecords = int(getFileInfo("maxRecords"))
if maxRecords <= 100000:
    num_threads = 1
elif maxRecords <= 200000:
    num_threads = 2
elif maxRecords <= 300000:
    num_threads = 3
elif maxRecords <= 500000:
    num_threads = 4
elif maxRecords <= 1000000:
    num_threads = 5
# Et ainsi de suite, en fonction du nombre de lignes de données en sortie

# Nom du fichier horodaté
path = getFileInfo("path")
filename = "%s\%s_%s.csv" % (path, getFileInfo("genre"), time.strftime(getFileInfo("dateFormat")))

# Les colonnes
fieldnames = getkeys(sectionName[0])

# Ouvrir le fichier csv en mode écriture
with open(filename, 'w', newline='') as csvfile:
    # Créer un écrivain csv
    writer = csv.writer(csvfile,delimiter=getFileInfo("delimiter"))
    # Écrire les en-têtes de colonne
    writer.writerow(fieldnames)

    # Diviser le travail en plusieurs threads
    threads = []
    for i in range(num_threads):
        start = i * (maxRecords // num_threads)
        end = (i + 1) * (maxRecords // num_threads)
        if i == num_threads - 1:
            end = maxRecords
        t = threading.Thread(target=write_data, args=(start, end, writer))
        threads.append(t)
        t.start()

    # Attendre que tous les threads aient fini
    for t in threads:
        t.join()

# Afficher le temps d'exécution et le nombre de lignes de données en sortie
end = time.time()
print("Le nombre de lignes est " + str(maxRecords) + " lignes")
print("CSV généré en " + str(end - star) + " secondes")
