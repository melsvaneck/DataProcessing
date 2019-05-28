#!/usr/bin/env python
# Name:mels van eck
# Student number:12505757
"""
This script converts CSV files.
"""
import csv
import sys
import pandas as pd
from datetime import datetime


def get_name():

    # check for correct usage
    if len(sys.argv) != 2:
        print("Usage: python convertCSV2JSON.py filename.csv")
        sys.exit(1)

    input_csv = sys.argv[1]

    return input_csv


def read_csv(input_csv):

    # make sure it prints all columns and rows
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    # read the csv file with pandas
    data = pd.read_csv(input_csv, delimiter=";", usecols=['Aantal_kasten',
                                                          'Aantal_volken',
                                                          'LAT',
                                                          'LNG'])

    return data

def make_csv(data):
    data.to_csv(r'Honey_bees', index=False)

def make_json(data):

    # make a json file
    data.to_json(r'Data.json', orient='index')


if __name__ == "__main__":

    make_csv(read_csv(get_name()))
