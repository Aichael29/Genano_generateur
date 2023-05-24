import csv
import random
from datetime import datetime, timedelta

def generate_csv_file(num_rows):
    columns = [
        "id_date", "dn", "date_debut", "type_even", "nombre_even", "even_minutes", "direction_appel",
        "termination_type", "type_reseau", "type_destination", "operator", "zone", "country",
        "profile_id", "city", "region", "gamme", "marche", "segment", "billing_type", "contract_id", "date_fin"
    ]

    rows = []
    for _ in range(num_rows):
        row = []
        # id_date
        id_date = random_date(datetime(2022, 1, 1), datetime(2023, 3, 31))
        row.append(id_date.strftime("%Y%m%d"))
        # dn
        dn = generate_dn()
        row.append(dn)
        # date_debut
        row.append(id_date.strftime("%Y-%m-%d %H:%M:%S"))
        # type_even
        type_even = random.choice(["voice", "sms"])
        row.append(type_even)
        # nombre_even
        row.append(random.randint(1, 10))
        # even_minutes
        if type_even == "sms":
            row.append(None)
            date_fin = id_date + timedelta(minutes=random.randint(1, 60))
        else:
            even_minutes = random.randint(1, 60)
            row.append(even_minutes)
            date_fin = id_date + timedelta(minutes=even_minutes)
        # direction_appel
        row.append(random.choice(["IN", "OUT"]))
        # termination_type
        row.append(random.choice(["on-net", "off-net"]))
        # type_reseau
        row.append(random.choice(["mobile", "fix"]))
        # type_destination
        type_destination = random.choice(["national", "international"])
        row.append(type_destination)
        # operator
        if type_destination == "international":
            row.append("International")
        else:
            row.append(random.choice(["INWI", "IAM", "ORANGE"]))
        # zone
        if row[-1] == "International":
            row.append(random.choice(["zone1", "zone2", "zone3", "zone4"]))
        else:
            row.append(random.choice(["Zone1", "Zone2", "Zone3", "Zone4", "Nationale Zone"]))
        # country
        if random.random() < 0.2:  # 20% chance of non-Maroc country
            row.append(random.choice(["Morocco", "France", "Spain", "USA"]))
        else:
            row.append("Morocco")
        # profile_id
        row.append(str(random.randint(1000, 9999)))
        # city
        row.append(random.choice(["Casablanca", "Rabat", "Marrakech", "Fes", "Tangier"]))
        # region
        row.append(random.choice(["Grand Casablanca", "Rabat-Sale-Kenitra", "Marrakech-Safi", "Fes-Meknes", "Tanger-Tetouan-Al Hoceima"]))
        # gamme
        row.append(random.choice(["Fibre optique", "ADSL", "MRE", "Data Prepaid", "Data Postpaid", "Forfaits 99 dhs",
                                  "Forfaits 49 dhs", "Forfaits 149 dhs", "Forfaits 199 dhs", "Forfaits 249 dhs"]))
        # marche
        if row[-2] == "B2B":
            row.append("mobile postpaid home")
        else:
            row.append(random.choice(["Mobile Prepaid", "Mobile Postpaid", "Home"]))
        # segment
        row.append(random.choice(["B2B", "B2C", "Autres"]))
        # billing_type
        if row[-1] == "B2B":
            row.append("Prepaid")
        else:
            row.append(random.choice(["Prepaid", "Postpaid", "Autres"]))
        # contract_id
        row.append("ABC" + str(random.randint(100000, 999999)))
        # date_fin
        row.append(date_fin.strftime("%Y-%m-%d %H:%M:%S"))

        rows.append(row)

    with open("data.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        writer.writerows(rows)

    print(f"CSV file with {num_rows} rows generated successfully!")

def random_date(start_date, end_date):
    return start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))

def generate_dn():
    prefix = "2125" if random.random() < 0.5 else "2126"
    suffix = str(random.randint(10000000, 99999999))
    return prefix + suffix

# Exemple d'utilisation
generate_csv_file(10)  # Génère un fichier CSV avec 10 lignes
