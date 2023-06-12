from fct import *
# Lecture des paramètres de configuration
num_rows = config.getint('data', 'num_rows')
output_file = config.get('data', 'output_file')

# Génération de la table de données
data_table = generate_data_table(num_rows)

# Sauvegarde des données dans un fichier CSV
save_data_to_csv(data_table, output_file)
