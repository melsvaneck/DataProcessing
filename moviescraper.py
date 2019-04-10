#!/usr/bin/env python
# Name:mels van eck
# Student number:12505757
"""
This script scrapes IMDB and outputs a CSV file with highest rated movies.
"""

import csv
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

TARGET_URL = "https://www.imdb.com/search/title?title_type=feature&release_date=2008-01-01,2018-01-01&num_votes=5000,&sort=user_rating,desc"
BACKUP_HTML = 'movies.html'
OUTPUT_CSV = 'movies.csv'


def extract_movies(dom):
    """
    Extract a list of highest rated movies from DOM (of IMDB page).
    Each movie entry should contain the following fields:
    - Title
    - Rating
    - Year of release (only a number!)
    - Actors/actresses (comma separated if more than one)
    - Runtime (only a number!)
    """

    dom.encode("utf-8")
    movies = []

    for title in dom.findAll("div", {"class": "lister-item mode-advanced"}):
        movie = {}
        movie["Title"] = title.h3.a.text
        for rating in title.findAll("span", {"class": "value"}):
            movie["Rating"] = float(rating.text)
        for year in title.findAll("span", {"class": "lister-item-year text-muted unbold"}):
            year = year.text
            year = year.replace('(', '').replace(')', '').replace('II', '')\
                        .replace('I', '')
            year = int(year)
            movie["Year"] = year
        actors = []
        for actor in title.select('a[href*=_st]'):
            actors.append(actor.text)
        actorsstring = "/".join(actors)
        movie["Actors"] = actorsstring
        for runtime in title.findAll("span", {"class": "runtime"}):
            runtime = (runtime.text).replace("min" , "")
            movie["Runtime"] = runtime
        movies.append(movie)
    return movies

def make_plot(movies):

    years = []
    averageRate = {}
    allrates = []
    new = {}
    # make a chronological list of all the years where movies where made
    for movie in movies:
        allrates.append(movies[movie]["rating"])
        if movies[movie]["year"] not in years:
            years.append(movies[movie]["year"])
            averageRate[movies[movie]["year"]] = [movies[movie]["rating"]]
        else:
            averageRate[movies[movie]["year"]].append(movies[movie]["rating"])
    years = sorted(years)
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
    plt.bar(range(len(new)), list(new.values()), align='center')
    plt.xticks(range(len(new)), list(new.keys()))
    plt.ylabel('ratings')
    plt.xlabel('years')


    plt.subplot(122)
    plt.scatter(range(len(new)), list(new.values()), color="red")
    plt.plot(range(len(new)), allrates)
    plt.xticks(range(len(new)), list(new.keys()))
    plt.ylim(0,10)
    plt.xlabel('years')
    plt.ylabel('ratings')

    plt.show()

def average(lst):
    return sum(lst) / len(lst)

def save_csv(outfile, movies):
    """
    Output a CSV file containing highest rated movies.
    """
    #
    # writer = csv.writer(outfile)
    # writer.writerow(['Title', 'Rating', 'Year', 'Actors', 'Runtime'])
    # for line in movies:
    #     writer.writerow(line)

    csv_columns = ['Title', 'Rating', 'Year', 'Actors', 'Runtime']

    try:
        with open(outfile, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in movies:
                writer.writerow(data)
    except IOError:
        print("I/O error")


    # ADD SOME CODE OF YOURSELF HERE TO WRITE THE MOVIES TO DISK


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print('The following error occurred during HTTP GET request to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


if __name__ == "__main__":

    # get HTML content at target URL
    html = simple_get("https://www.imdb.com/search/title?title_type=feature&release_date=2008-01-01,2018-01-01&num_votes=5000,&sort=user_rating,desc")

    # save a copy to disk in the current directory, this serves as an backup
    # of the original HTML, will be used in grading.
    with open(BACKUP_HTML, 'wb') as f:
        f.write(html)
    # parse the HTML file into a DOM representation
    dom = BeautifulSoup(html, 'html.parser')

    # extract the movies (using the function you implemented)
    movies = extract_movies(dom)

    # write the CSV file to disk (including a header)
    # with open(OUTPUT_CSV, 'w', newline='') as output_file:
    save_csv("movies.csv", movies)
