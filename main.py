import csv
import random
from datetime import datetime, timedelta
dn_contract_map = {}

def generate_csv_file(num_rows):
    columns = [
        "id_date", "dn", "date_debut", "type_even", "nombre_even", "even_minutes", "direction_appel",
        "termination_type", "type_reseau", "type_destination", "operator", "country",
        "profile_id", "city", "segment", "billing_type", "gamme", "marche", "contract_id", "date_fin"
    ]
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2023, 3, 1)
    segment_set = set()
    billing_type_set = set()
    gamme_set = set()
    marche_set = set()

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
        row.append(id_date.strftime("%d/%m/%Y %H:%M:%S"))
        # type_even
        type_even=""
        if dn[3] == '5':
            type_even="voice"
        else:
            type_even=random.choice(["sms", "voice"])
        row.append(type_even)
        # nombre_even
        row.append(random.randint(1, 10))
        # even_minutes
        if type_even == "sms":
            row.append(None)
            date_fin = id_date + timedelta(minutes=random.randint(1, 60))
        else:
            even_minutes = round(random.uniform(1, 60), 2)
            row.append(even_minutes)
            date_fin = id_date + timedelta(minutes=even_minutes)
        # direction_appel
        row.append(random.choice(["IN", "OUT"]))
        # termination_type
        termination_type = random.choices(["on-net", "off-net"], [0.35, 0.65])[0]
        row.append(termination_type)
        # type_reseau
        if type_even == "sms":
            row.append("mobile")
        else:
            row.append(random.choices(["mobile", "fix"],[0.65, 0.35])[0])
        # type_destination + operator + country
        if termination_type == "on-net":
            type_destination = "national"
            operator = "INWI"
            country = "Morocco"
        else:
            type_destination = random.choices(["national", "international"], [0.81, 0.19])[0]
            if type_destination == "national":
                operator = random.choices(["IAM", "ORANGE"], [0.52, 0.48])[0]
            else:
                operator = "International"
            if operator == "International":
                country = random.choices(
                    ["France", "Spain", "USA", "Liechtenstein", "Allemagne", "Lituanie", "Autriche", "Luxembourg",
                     "Australie", "Arabie Saoudite", "Mali", "Belgique", "Sénégal"],
                    [0.60, 0.20, 0.05, 0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01])[0]
            else:
                country = "Morocco"
        row.append(type_destination)
        row.append(operator)
        row.append(country)

        # profile_id
        row.append(str(random.randint(1000, 9999)))
        # city
        if type_destination == "national":
            row.append(random.choice(["Casablanca", "Rabat", "Marrakech", "Fes", "Tangier"]))
        else:
            row.append("international city")
            # segment
            segment = random.choices(["B2B", "B2C"], [0.30, 0.70])[0]
            while segment in segment_set:
                segment = random.choices(["B2B", "B2C"], [0.30, 0.70])[0]
            segment_set.add(segment)
            row.append(segment)

            # billing_type
            billing_type = ""
            if row[8] == "fix":
                billing_type = "postpaid"
            elif segment == "B2B":
                billing_type = random.choices(["postpaid", "prepaid", "Autres"], [0.97, 0.02, 0.01])[0]
            elif segment == "B2C":
                billing_type = random.choices(["postpaid", "prepaid", "Autres"], [0.19, 0.80, 0.01])[0]
            while billing_type in billing_type_set:
                if row[8] == "fix":
                    billing_type = "postpaid"
                elif segment == "B2B":
                    billing_type = random.choices(["postpaid", "prepaid", "Autres"], [0.97, 0.02, 0.01])[0]
                elif segment == "B2C":
                    billing_type = random.choices(["postpaid", "prepaid", "Autres"], [0.19, 0.80, 0.01])[0]
            billing_type_set.add(billing_type)
            row.append(billing_type)

            # gamme
            gamme = ""
            if row[8] == "fix":
                gamme = random.choice(["ADSL", "Fibre optique"])
            elif row[8] == "mobile":
                if billing_type == "prepaid":
                    gamme = "Data Prepaid"
                else:
                    gamme = random.choice(["MRE", "Data Postpaid", "Forfaits 99 dhs", "Forfaits 49 dhs",
                                           "Forfaits 149 dhs", "Forfaits 199 dhs", "Forfaits 249 dhs"])
            while gamme in gamme_set:
                if row[8] == "fix":
                    gamme = random.choice(["ADSL", "Fibre optique"])
                elif row[8] == "mobile":
                    if billing_type == "prepaid":
                        gamme = "Data Prepaid"
                    else:
                        gamme = random.choice(["MRE", "Data Postpaid", "Forfaits 99 dhs", "Forfaits 49 dhs",
                                               "Forfaits 149 dhs", "Forfaits 199 dhs", "Forfaits 249 dhs"])
            gamme_set.add(gamme)
            row.append(gamme)

            # marche
            marche = ""
            if gamme == "Data Prepaid":
                marche = "Mobile Prepaid"
            elif gamme == "Data Postpaid":
                marche = "Mobile Postpaid"
            elif gamme in ["MRE", "Forfaits 99 dhs", "Forfaits 49 dhs",
                           "Forfaits 149 dhs", "Forfaits 199 dhs", "Forfaits 249 dhs"]:
                marche = "Mobile Consumer"
            while marche in marche_set:
                if gamme == "Data Prepaid":
                    marche = "Mobile Prepaid"
                elif gamme == "Data Postpaid":
                    marche = "Mobile Postpaid"
                elif gamme in ["MRE", "Forfaits 99 dhs", "Forfaits 49 dhs",
                               "Forfaits 149 dhs", "Forfaits 199 dhs", "Forfaits 249 dhs"]:
                    marche = "Mobile Consumer"
            marche_set.add(marche)
            row.append(marche)


        # contract_id
        contract_id = dn_contract_map.get(dn)
        if contract_id is None:
            contract_id = "ABC" + str(random.randint(100000, 999999))
            dn_contract_map[dn] = contract_id
        row.append(contract_id)
        # date_fin
        row.append(date_fin.strftime("%d/%m/%Y %H:%M:%S"))

        rows.append(row)

    with open("C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/traffic.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        writer.writerows(rows)


def generate_dn():
    phone_numbers = [
        "212682545893", "212557677120", "212639978793", "212565008502", "212647283807",
        "212592829599", "212611849600", "212515133772", "212587904894", "212577878936",
        "212669941847", "212698478830", "212546350385", "212677642025", "212664557773",
        "212574132800", "212599466801", "212548264984", "212521202409", "212679922956",
        "212534281712", "212614704227", "212642091826", "212661358387", "212578568092",
        "212517492422", "212594697743", "212557513277", "212641880505", "212616757810",
        "212525897686", "212655434376", "212565073822", "212663208000", "212613015250",
        "212681884363", "212654729798", "212565544721", "212693680492", "212671776707",
        "212693662807", "212613486147", "212636573489", "212642219476", "212635101016",
        "212640797824", "212580488980", "212510966909", "212669283431", "212683456974",
        "212557192252", "212584883647", "212561936803", "212610868217", "212623339588",
        "212680153550", "212654208815", "212635465564", "212678637785", "212518950595",
        "212619414904", "212676384026", "212655274351", "212691811290", "212691277113",
        "212527278290", "212665990317", "212537475969", "212647844537", "212595972547",
        "212585959717", "212667372713", "212593796083", "212697435132", "212513289563",
        "212662262352", "212670387501", "212513799198", "212618260623", "212544139035",
        "212650397447", "212536113438", "212582766856", "212525178369", "212687136939",
        "212655340643", "212650414410", "212628109474", "212617203015", "212518140965",
        "212696944550", "212578325844", "212682845829", "212653210149", "212642698374",
        "212652517294", "212648526213", "212546077839", "212665760842", "212574633393"
    ]
    return random.choice(phone_numbers)



# Exemple d'utilisation
generate_csv_file(1000)  # Génère un fichier CSV avec x lignes
