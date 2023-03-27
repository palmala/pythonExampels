import random
import datetime
import csv

countries = ['HUN', 'GER', 'FRA']
counties = {
    "HUN": ['hun_county1', 'hun_county2'],
    "GER": ['ger_county1', 'ger_county2'],
    'FRA': ['ger_county1', 'ger_county2']
}
cities = {
    'hun_county1': ['huncity11', 'huncity12'],
    'hun_county2': ['huncity21', 'huncity22'],
    'ger_county1': ['gercity11', 'gercity12'],
    'ger_county2': ['gercity21', 'gercity22'],
    'fra_county1': ['gercity11', 'gercity12'],
    'fra_county2': ['fracity21', 'fracity22']
}


def main():
    today = datetime.date.today().strftime("%Y%m%d")


if __name__ == "__main__":
    main()


