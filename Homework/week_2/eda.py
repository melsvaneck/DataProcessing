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
import pandas as pd
from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import FormatStrFormatter
INPUT_CSV = "input.csv"


def get_data():
    # makes it print all the data in my command line
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    # select only the columns that i need to select
    data = pd.read_csv(INPUT_CSV, usecols=['Country',
                                           'Region',
                                           'Pop. Density (per sq. mi.)',
                                           'Infant mortality (per 1000 births)',
                                           'GDP ($ per capita) dollars'])

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

    return DataFrame(data)


def Get_mean(data):

    # Getting the mean,medioan and mode from the data
    meanGDP = round(data['GDP ($ per capita) dollars'].mean(skipna=True), 2)
    modeGDP = data['GDP ($ per capita) dollars'].mode()[0]
    medianGDP = data.loc[:, 'GDP ($ per capita) dollars'].median()

    # print the data
    print(f"Mean:{meanGDP}")
    print(f"Mode:{modeGDP}")
    print(f"median:{medianGDP}")


def plot_histogram(data):

    plot = data.hist(column='GDP ($ per capita) dollars', bins=75, grid=False,
                     figsize=(12, 8), color='#86bf91', zorder=2, rwidth=0.9)

    plot = plot[0]
    for x in plot:

        # Despine
        x.spines['right'].set_visible(False)
        x.spines['top'].set_visible(False)
        x.spines['left'].set_visible(False)

        # Switch off ticks
        x.tick_params(axis="both", which="both", bottom="off", top="off",
                      labelbottom="on",  left="off", right="off", labelleft="on")

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


if __name__ == "__main__":

    data = get_data()
    Get_mean(data)
    plot_histogram(data)
