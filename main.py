import csv
import random
from datetime import datetime, timedelta

operator = random.choice(["INWI", "IAM", "ORANGE", "International"])
def generate_csv_file(num_rows):
    columns = [
        "id_date", "dn", "date_debut", "type_even", "nombre_even", "even_minutes", "direction_appel",
        "termination_type", "type_reseau", "type_destination", "operator","country",
        "profile_id", "city", "gamme", "marche", "segment", "billing_type", "contract_id", "date_fin"
    ]
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2023, 3, 1)

    rows = []
    for _ in range(num_rows):
        row = []
        # id_date
        id_date = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
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
        type_reseau=random.choice(["mobile", "fix"])
        row.append(type_reseau)
        # type_destination
        type_destination = random.choice(["national", "international"])
        choices = ["national", type_destination]
        weights = [0.7, 0.3]
        row.append(random.choices(choices, weights)[0])
        # operator
        if type_destination == "national":
            row.append(random.choice(["INWI", "IAM", "ORANGE"]))
        elif type_destination == "international":
            row.append("International")

        # country
        if type_destination == "national":
            row.append("Morocco")
        else:
            row.append(random.choice(["France", "Spain", "USA"]))

        # profile_id
        row.append(str(random.randint(1000, 9999)))
        # city
        if type_destination == "national" and operator in ["INWI", "IAM", "ORANGE"]:  # 20% chance of non-Maroc cities
            row.append(random.choice(["Casablanca", "Rabat", "Marrakech", "Fes", "Tangier"]))
        else:
            row.append("international city")
        # gamme
        gamme=random.choice(["Fibre optique", "ADSL", "MRE", "Data Prepaid", "Data Postpaid", "Forfaits 99 dhs",
                       "Forfaits 49 dhs", "Forfaits 149 dhs", "Forfaits 199 dhs", "Forfaits 249 dhs"])
        row.append(gamme)

        # marche
        marche=random.choice(["Mobile Prepaid", "Mobile Postpaid","Home"])
        if type_reseau == "mobile":
            row.append(random.choice(["Mobile Prepaid", "Mobile Postpaid"]))
        elif type_reseau == "Fix":
            row.append(random.choice(["Home", "Mobile Postpaid"]))
        elif gamme == "Data Prepaid":
            row.append("Mobile Prepaid")
        elif gamme == "Data Postpaid":
            row.append("Mobile Postpaid")
        elif gamme == "MRE":
            row.append(random.choice(["Mobile Prepaid", "Mobile Postpaid"]))
        elif gamme == "ADSL" or gamme == "Fibre optique":
            row.append("Home")
        else:
            row.append(marche)

        # segment
        segment = random.choice(["B2B", "B2C", "Autres"])
        if marche == "Mobile Prepaid":
            choices = ["B2C", segment]
            weights = [0.99, 0.01]  # Les poids déterminent la probabilité de chaque choix
            row.append(random.choices(choices, weights)[0])
        elif marche == "Mobile Postpaid":
            choices = ["B2B", segment]
            weights = [0.99, 0.01]  # Les poids déterminent la probabilité de chaque choix
            row.append(random.choices(choices, weights)[0])
        else:
            row.append(segment)

        # billing_type
        if marche == "Mobile Postpaid":
            row.append("postpaid")
        elif marche == "Mobile Prepaid":
            row.append("prepaid")
        else:
            row.append("Autres")

        # contract_id
        row.append("ABC" + str(random.randint(100000, 999999)))
        # date_fin
        row.append(date_fin.strftime("%Y-%m-%d %H:%M:%S"))

        rows.append(row)

    with open("Traffic data.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        writer.writerows(rows)


def generate_dn():
    prefix = "2125" if random.random() < 0.5 else "2126"
    suffix = str(random.randint(10000000, 99999999))
    return prefix + suffix

# Exemple d'utilisation
generate_csv_file(10000)  # Génère un fichier CSV avec 10000 lignes