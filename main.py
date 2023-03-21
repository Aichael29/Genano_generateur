import time
import os
import traceback
from openpyxl import Workbook
from getters import * # Importing all of functions from our library getters.py

start = time.time()

# Nom du fichier horodaté
dateFile = time.strftime(getFileInfo("dateFormat"))
fileType = getFileInfo("fileType")
filename = "%s_%s.%s" % (getFileInfo("genre"), dateFile, fileType)

# le nombre d'enregistrement à partir de la section FileInfo
maxRecords = int(getFileInfo("maxRecords"))

wb = Workbook()
ws = wb.active

try:
    ws.append(fieldnames)
    for i in range(0, maxRecords):
        row = []
        for field in fieldnames:
            row.append(getData(field))
        ws.append(row)

    wb.save(filename)

except:
    os.remove(filename) # Remove file if any error occurs
    traceback.print_exc()

end = time.time()
print("XLSX généré en "+ str(end - start) +" secondes")
