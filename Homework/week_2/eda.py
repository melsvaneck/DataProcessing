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

    # remove all the "dollars" texts and replace comma's with points in the columns
    data['GDP ($ per capita) dollars'].replace(regex=True,
                                               inplace=True,
                                               to_replace=r'\D',
                                               value=r'')
    data['Pop. Density (per sq. mi.)'].replace(regex=True,
                                               inplace=True,
                                               to_replace=r',',
                                               value=r'.')
    data['Infant mortality (per 1000 births)'].replace(regex=True,
                                                       inplace=True,
                                                       to_replace=r',',
                                                       value=r'.')

    # make the datatype of GDP,Density and Infant mortality numeric
    data['Infant mortality (per 1000 births)'] = \
        pd.to_numeric(data['Infant mortality (per 1000 births)'], errors='coerce')
    data['GDP ($ per capita) dollars'] = \
        pd.to_numeric(data['GDP ($ per capita) dollars'], errors='coerce')
    data['Pop. Density (per sq. mi.)'] = \
        pd.to_numeric(data['Pop. Density (per sq. mi.)'], errors='coerce')

    # getting rid of the false values
    # proof: http://statisticstimes.com/economy/projected-world-gdp-capita-ranking.php
    data['GDP ($ per capita) dollars'].where(
        (data['GDP ($ per capita) dollars'] < 150000), inplace=True)

    return data


def plot_boxplot(data):

    # Getting the mean,median and mode from the infant mortality column
    five_numsum = data['Infant mortality (per 1000 births)'].describe()
    print("Five number summarry of the Infant mortality\n" +
          f"Minimum value: {round(five_numsum['min'],2)}\n" +
          f"First quartile: {round(five_numsum['25%'],2)}\n" +
          f"Median: {round(five_numsum['50%'],2)}\n" +
          f"Third quartile: {round(five_numsum['75%'],2)}\n" +
          f"Maximum value: {round(five_numsum['max'],2)}\n")

    # making the boxplot of the infant mortality
    ax = data.boxplot(column='Infant mortality (per 1000 births)')

    # set amount of ticks and instances
    plt.yticks(np.arange(0, 210, 10))

    # set title
    ax.set_title("Infant mortality")

    # set labels
    ax.set_ylabel("Amount", labelpad=20, weight='bold', size=12)

    plt.show()


def plot_histogram(data):
    # Getting the mean,medioan and mode from the GDP column
    meanGDP = round(data['GDP ($ per capita) dollars'].describe()['mean'], 2)
    modeGDP = data['GDP ($ per capita) dollars'].mode()[0]
    medianGDP = data['GDP ($ per capita) dollars'].describe()['50%']

    # print the data
    print(f"The mean, mode and median of the GDP ($ per capita) \n" +
          f"Mean:{meanGDP}\n" +
          f"Mode:{modeGDP}\n" +
          f"Median:{medianGDP}\n")

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

        # set title
        x.set_title("GDP ($ per capita) in dollars")

        # Set axis labels
        x.set_xlabel('Dollars', labelpad=20, weight='bold', size=12)
        x.set_ylabel("Number of countries", labelpad=20, weight='bold', size=12)

        plt.show()


def make_json(data):

    # set the index to Countrty
    data.set_index('Country', inplace=True)

    # make a json file
    data.to_json(r'D.json', orient='index')


if __name__ == "__main__":

    data = get_data()
    plot_histogram(data)
    plot_boxplot(data)
    make_json(data)
