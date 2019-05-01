#!/usr/bin/env python
# Name:mels van eck
# Student number:12505757
"""
This script converts CSV files to a JSON file.
"""
import csv
import sys
import pandas as pd


def get_name():

    # check for correct usage
    if len (sys.argv) != 2 :
        print("Usage: python convertCSV2JSON.py filename.csv")
        sys.exit (1)

    input_csv = sys.argv[1]

    return input_csv

def read_csv(input_csv):

    # make sure it prints all columns and rows
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    # read the csv file with pandas
    data = pd.read_csv(input_csv,delimiter=";", usecols = ['Locatie',
                                                           'Type_knelpunt',
                                                           'Diersoorten',
                                                           'Type_oplossing',
                                                           'Jaar_realisatie'])

    data['Jaar_realisatie'] = \
        pd.to_numeric(data['Jaar_realisatie'], errors='coerce')

    data['Jaar_realisatie'] = data['Jaar_realisatie'].replace(0,"Nan")

    data['Diersoorten'] = data['Diersoorten'].str.split("-")



    return data

def make_json(data):

    # make a json file
    data.to_json(r'Data.json', orient='index')

if __name__ == "__main__":


    make_json(read_csv(get_name()))
