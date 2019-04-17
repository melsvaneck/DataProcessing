#!/usr/bin/env python
# Name:Mels van Eck
# Student number:12505757
"""
This script visualizes data obtained from a .csv file
it will show: “Country”, “Region”,
 “Pop. Density (per sq. mi.)”,
 “Infant mortality (per 1000 births)”
 and “GDP ($ per capita) dollars”.
"""

import csv
import math
import json
import pandas as pd
from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import FormatStrFormatter
INPUT_CSV = "input.csv"


def get_data():
    # select only the columns that i need to select
    data = pd.read_csv(INPUT_CSV, usecols=['Country',
                                           'Region',
                                           'Pop. Density (per sq. mi.)',
                                           'Infant mortality (per 1000 births)',
                                           'GDP ($ per capita) dollars'])

    # set the index to Countrty
    data.set_index('Country',inplace = True)

    # remove all the "dollars" texts and replace comma's with points in the columns
    data['GDP ($ per capita) dollars'].replace(regex=True, inplace=True,
                                               to_replace=r'\D', value=r'')
    data['Pop. Density (per sq. mi.)'].replace(regex=True, inplace=True,
                                               to_replace=r',', value=r'.')
    data['Infant mortality (per 1000 births)'].replace(regex=True, inplace=True,
                                                       to_replace=r',', value=r'.')


    # make the datatype of GDP,Density and Infant mortality numeric
    data['GDP ($ per capita) dollars'] = \
        pd.to_numeric(data['GDP ($ per capita) dollars'], errors='coerce')

    data['Pop. Density (per sq. mi.)'] = \
        pd.to_numeric(data['Pop. Density (per sq. mi.)'], errors='coerce')

    data['Infant mortality (per 1000 births)'] = \
        pd.to_numeric(data['Infant mortality (per 1000 births)'], errors='coerce')

    # getting rid of the false values
    # proof: http://statisticstimes.com/economy/projected-world-gdp-capita-ranking.php
    data.where((data['GDP ($ per capita) dollars'] < 150000), inplace=True)

    return data

def plot_boxplot(data):


    # Getting the mean,medioan and mode from the infant mortality column
    numsum = data['Infant mortality (per 1000 births)'].describe()
    print(f"Minimum value: {numsum['min']}")
    print(f"First quartile: {numsum['25%']}")
    print(f"Median: {numsum['50%']}")
    print(f"Third quartile: {numsum['75%']}")
    print(f"Maximum value: {numsum['max']}")

    data.boxplot(column = 'Infant mortality (per 1000 births)')

    plt.show()

def plot_histogram(data):
    # Getting the mean,medioan and mode from the GDP column
    meanGDP = round(data['GDP ($ per capita) dollars'].describe()['mean'], 2)
    modeGDP = data['GDP ($ per capita) dollars'].mode()[0]
    medianGDP = data['GDP ($ per capita) dollars'].describe()['50%']

    # print the data
    print("GDP Data")
    print(f"Mean:{meanGDP}")
    print(f"Mode:{modeGDP}")
    print(f"Median:{medianGDP}")
    print()

    # make a histogram
    plot = data.hist(column='GDP ($ per capita) dollars', bins=75, grid=False,
                     figsize=(12, 8), color='#86bf91', zorder=2, rwidth=0.9)

    plot = plot[0]
    for x in plot:

        # Despine
        x.spines['right'].set_visible(False)
        x.spines['top'].set_visible(False)
        x.spines['left'].set_visible(False)

        # Switch off ticks
        x.tick_params(axis="both", which="both", bottom=False, top=False,
                      labelbottom=True,  left=False, right=False, labelleft=True)

        # Draw horizontal axis lines
        vals = x.get_yticks()
        for tick in vals:
            x.axhline(y=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)

        # Remove title
        x.set_title("GDP ($ per capita) in dollars")

        # Set axis labels
        x.set_xlabel('Dollars', labelpad=20, weight='bold', size=12)
        x.set_ylabel("Number of countries", labelpad=20, weight='bold', size=12)

        plt.show()

def make_json(data):

 # make a json file
 data.to_json(r'D.json',orient = 'index')


if __name__ == "__main__":

    data = get_data()
    plot_histogram(data)
    plot_boxplot(data)
    make_json(data)
