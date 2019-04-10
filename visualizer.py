#!/usr/bin/env python
# Name:
# Student number:
"""
This script visualizes data obtained from a .csv file
"""

import csv
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import FormatStrFormatter
import numpy as np


# Global constants for the input file, first and last year
INPUT_CSV = "movies.csv"

def make_plot(movies):
    years = []
    averageRate = {}
    allrates = []
    new = {}


    for movie in movies:
        # Make a list of all the ratings for a total average
        allrates.append(movies[movie]["Rating"])
        # make a dict of all the years in wich the movies where made as keys
        # the values are all the ratings in that year
        if movies[movie]["Year"] not in years:
            years.append(movies[movie]["Year"])
            averageRate[movies[movie]["Year"]] = [movies[movie]["Rating"]]
        else:
            averageRate[movies[movie]["Year"]].append(movies[movie]["Rating"])

    # sort the list of years in chronological order
    years = sorted(years)
    # calculate the total average
    totalavg = average(allrates)
    totalavg = round(totalavg,2)

    allrates = []
    # make the an average number of the rating list
    for year in averageRate:
        ratings = averageRate[year]
        averageRate[year] = average(ratings)
        averageRate[year] = round(averageRate[year],2)
        allrates.append(totalavg)

    for year in years:
        new[year] = averageRate[year]

    plt.figure(figsize=(12,4))
    plt.subplot(121)
    plt.plot(range(len(new)), list(new.values()))
    plt.xticks(range(len(new)), list(new.keys()))
    plt.yticks(np.arange(0, 11, 1.0))
    plt.ylabel('ratings')
    plt.xlabel('years')
    plt.grid(True)

    plt.subplot(122)
    red_patch = mpatches.Patch(color='red', label='yearly avg.')
    blue_patch = mpatches.Patch(color='blue', label='total avg.')
    plt.legend(handles=[red_patch,blue_patch])
    plt.scatter(range(len(new)), list(new.values()), color="red")
    plt.plot(range(len(new)), allrates)
    plt.xticks(range(len(new)), list(new.keys()))
    plt.yticks(np.arange(7, 10, 0.3))
    plt.xlabel('years')
    plt.ylabel('ratings')
    plt.grid(True)

    plt.show()

def average(lst):
    return sum(lst) / len(lst)



if __name__ == "__main__":

    movies = {}
    with open(INPUT_CSV, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            movie = {}
            movie["Year"] = int(row["Year"])
            movie["Rating"] = float(row["Rating"])
            movie["Runtime"] = row["Runtime"]
            movie["Actors"] = row["Actors"]
            movies[row["Title"]] = movie

    make_plot(movies)
