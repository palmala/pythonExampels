import random
from datetime import datetime, timedelta
import csv

developers = ['Doe, Jane', 'Doe, John']


def random_time_window():
    sdate = datetime(2022, 1, 1) + timedelta(days=random.randrange(1, 364))
    edate = sdate + timedelta(hours=random.randrange(2, 168))
    return sdate, edate


def main():
    leaves = list()
    for leave_id in range(100):
        start_date, end_date = random_time_window()
        leave = {'LEAVE_ID': leave_id, 'DEVELOPER': random.choice(developers), 'START_DATE': start_date,
                 'END_DATE': end_date}
        leaves.append(leave)
        print(leave)
    leaves = sorted(leaves, key=lambda d: d['START_DATE'])

    with open('leaves.csv', 'w', newline='') as outfile:
        dict_writer = csv.DictWriter(outfile, leaves[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(leaves)


if __name__ == "__main__":
    main()
