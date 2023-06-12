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
            'type_destination': generate_value_from_list(config.get('data', 'destination_types').split(',')),
            'operator': generate_value_from_list(config.get('data', 'operators').split(',')),
            'country': '',
            'profile_id': generate_value_from_list(config.get('data', 'profile_ids').split(',')),
            'city': '',
            'gamme': generate_value_from_list(config.get('data', 'gammes').split(',')),
            'marche': generate_value_from_list(config.get('data', 'marches').split(',')),
            'segment': generate_value_from_list(config.get('data', 'segments').split(',')),
            'billing_type': generate_value_from_list(config.get('data', 'billing_types').split(',')),
            'contract_id': config.get('data', 'contract_id_prefix') + str(random.randint(0, config.getint('data', 'max_contract_id'))),
            'last_timestamp': ''
        }

        if row['operator'] == 'INTERNATIONAL':
            row['country'] = generate_value_from_list([c for c in config.get('data', 'country').split(',') if c != 'Morocco'])
            row['city'] = 'international city'
        else:
            row['country'] = 'Morocco'
            row['city'] = generate_value_from_list(config.get('data', 'city').split(','))

        if row['type_even'] == 'sms':
            row['type_reseau'] = 'mobile'

        if row['type_even'] == 'voice':
            row['nombre_even'] = 1
        elif row['type_even'] == 'sms':
            row['even_minutes'] = 0

        row['last_timestamp'] = (datetime.strptime(row['date_debut'], '%Y-%m-%d %H:%M:%S') + timedelta(minutes=row['even_minutes'])).strftime('%Y-%m-%d %H:%M:%S')
        row['id_date'] = row['date_debut'].split()[0].replace('-', '')

        data_table.append(row)
    return data_table

# Fonction pour sauvegarder la table de données dans un fichier CSV
def save_data_to_csv(data_table, filename):
    fieldnames = data_table[0].keys()
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_table)


