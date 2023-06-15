import configparser
from datetime import datetime, timedelta
import random
import csv

# Chargement de la configuration
config = configparser.ConfigParser()
config.read('config.conf')


# Fonction pour générer un numéro de téléphone aléatoire
def generate_phone_number():
    prefix = config.get('data', 'phone_prefix')
    number = ''.join(random.choice('0123456789') for _ in range(9))
    return prefix + number


# Fonction pour générer une date aléatoire
def generate_date():
    start_date = datetime.strptime(config.get('data', 'start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(config.get('data', 'end_date'), '%Y-%m-%d')
    delta = (end_date - start_date).days
    random_days = random.randint(0, delta)
    return (start_date + timedelta(days=random_days)).strftime('%Y%m%d')


# Fonction pour générer un timestamp aléatoire
def generate_timestamp():
    start_timestamp = datetime.strptime(config.get('data', 'start_timestamp'), '%Y-%m-%d %H:%M:%S')
    end_timestamp = datetime.strptime(config.get('data', 'end_timestamp'), '%Y-%m-%d %H:%M:%S')
    delta = (end_timestamp - start_timestamp).total_seconds()
    random_seconds = random.uniform(0, delta)
    return (start_timestamp + timedelta(seconds=random_seconds)).strftime('%Y-%m-%d %H:%M:%S')


# Fonction pour générer une durée aléatoire en minutes
def generate_minutes():
    return round(random.uniform(0, config.getfloat('data', 'max_minutes')), 2)


# Fonction pour générer une valeur aléatoire à partir d'une liste
def generate_value_from_list(values):
    return random.choice(values)


# Fonction pour générer la table de données
def generate_data_table(num_rows):
    data_table = []
    for _ in range(num_rows):
        row = {
            'id_date': generate_date(),
            'dn': generate_phone_number(),
            'date_debut': generate_timestamp(),
            'type_even': generate_value_from_list(config.get('data', 'event_types').split(',')),
            'nombre_even': random.randint(0, config.getint('data', 'max_events')),
            'even_minutes': generate_minutes(),
            'direction_appel': generate_value_from_list(config.get('data', 'call_directions').split(',')),
            'termination_type': generate_value_from_list(config.get('data', 'termination_types').split(',')),
            'type_reseau': generate_value_from_list(config.get('data', 'network_types').split(',')),
            'type_destination': '',
            'operator': '',
            'country': '',
            'profile_id': random.randint(1000, 9999),
            'city': '',
            'gamme': '',
            'marche': '',
            'segment':'',
            'billing_type': '',
            'contract_id': '',
            'last_timestamp': ''
        }
        if row['termination_type'] == 'on-net':
            row['operator'] = 'NATIONAL'
            row['type_destination'] = 'national'
            row['operator'] = 'INWI'
        else:
            row['operator'] = generate_value_from_list(config.get('data', 'operators').split(','))

        if row['operator'] == 'INTERNATIONAL':
            row['type_destination'] = 'international'
            row['country'] = generate_value_from_list([c for c in config.get('data', 'country').split(',') ])
            row['city'] = 'international city'
        else:
            row['type_destination'] = 'national'
            row['country'] = 'Morocco'
            row['city'] = generate_value_from_list(config.get('data', 'city').split(','))

        if row['type_even'] == 'sms':
            row['type_reseau'] = 'mobile'

        if row['type_even'] == 'voice':
            row['nombre_even'] = 1
        elif row['type_even'] == 'sms':
            row['even_minutes'] = 0

        row['last_timestamp'] = (datetime.strptime(row['date_debut'], '%Y-%m-%d %H:%M:%S') + timedelta(
            minutes=row['even_minutes'])).strftime('%Y-%m-%d %H:%M:%S')
        row['id_date'] = row['date_debut'].split()[0].replace('-', '')
        if row['type_reseau'] == 'fix':
            row['gamme'] = random.choice(['Fibre optique', 'ADSL'])
        if row['type_reseau'] == 'mobile':
            row['gamme'] = generate_value_from_list(config.get('data', 'gammes').split(','))
        if row['gamme'] == 'Fibre optique' or row['gamme'] == 'ADSL':
            row['marche'] = 'home'
        elif row['gamme'] == 'Data Postpaid':
            row['marche'] = 'Mobile Postpaid'
        elif row['gamme'] == 'MRE':
            row['marche'] = random.choice(['Mobile Prepaid', 'Mobile Postpaid'])
        elif row['gamme'] == 'Data Prepaid' :
            row['marche'] = 'Mobile Prepaid'

        else:
            row['marche']= generate_value_from_list(config.get('data', 'marches').split(','))

        if row['marche'] == 'Mobile Prepaid':
            row['billing_type'] = 'prepaid'
        else:
            row['billing_type'] = 'postpaid'
        if row['billing_type'] == 'prepaid':
            row['segment'] = 'B2B' if random.random() < 0.1 else 'B2C'
        elif row['billing_type'] == 'postpaid':
            row['segment'] = 'B2B' if random.random() < 0.1 else 'B2C'



        row['contract_id'] = config.get('data', 'contract_id_prefix') + str(random.randint(0, config.getint('data', 'max_contract_id')))

        data_table.append(row)
    return data_table


# Fonction pour sauvegarder la table de données dans un fichier CSV
def save_data_to_csv(data_table, filename):
    fieldnames = data_table[0].keys()
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_table)


# Génération des données et sauvegarde dans un fichier CSV
num_rows = config.getint('data', 'num_rows')
data_table = generate_data_table(num_rows)
output_file = config.get('data', 'output_file')
save_data_to_csv(data_table, output_file)
