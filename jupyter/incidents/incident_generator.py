import random
import datetime
import csv

countries = ['HUN', 'GER', 'ENG', 'ITA', 'FRA']
category_values = ['Y', 'N']


def random_date():
    sdate = datetime.date(2021, 1, 1)
    edate = datetime.date(2023, 1, 31)
    pdate = sdate + random.random() * (edate - sdate)
    return f"{pdate.year}-{pdate.month}"


def main():
    incidents = list()
    for incident_id in range(100):
        incident = {'INCIDENT_ID': incident_id, 'DATE': random_date(), 'COUNTRY': random.choice(countries),
                    'CATEGORY1': random.choice(category_values), 'CATEGORY2': random.choice(category_values)}
        incidents.append(incident)

    with open('incidents.csv', 'w', newline='') as outfile:
        dict_writer = csv.DictWriter(outfile, incidents[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(incidents)


if __name__ == "__main__":
    main()
