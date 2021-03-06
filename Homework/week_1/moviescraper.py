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
    movies = []
    # Loop through the html-page and put all data per movie in a dictionary
    for title in dom.findAll("div", {"class": "lister-item mode-advanced"}):
        movie = {}
        movie["Title"] = title.h3.a.text
        for rating in title.findAll("span", {"class": "value"}):
            movie["Rating"] = float(rating.text)
        for year in title.findAll("span",
                                  {"class": "lister-item-year text-muted unbold"}):
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
            runtime = (runtime.text).replace("min", "")
            movie["Runtime"] = runtime
        # append all the movie dictionaries to a list
        movies.append(movie)

    return movies


def save_csv(outfile, movies):
    """
    Output a CSV file containing highest rated movies.
    """
    # make the first row for the collumn names
    csv_columns = ['Title', 'Rating', 'Year', 'Actors', 'Runtime']

    # write the list of the movies to the csv file
    try:
        with open(outfile, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in movies:
                writer.writerow(data)
    except IOError:
        print("I/O error")


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
        print('The following error occurred during HTTP GET request\
               to {0} : {1}'.format(url, str(e)))
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
    html = simple_get(
        "https://www.imdb.com/search/title?title_type=feature&release_date=2008-01-01,2018-01-01&num_votes=5000,&sort=user_rating,desc")

    # save a copy to disk in the current directory, this serves as an backup
    # of the original HTML, will be used in grading.
    with open(BACKUP_HTML, 'wb') as f:
        f.write(html)
    # parse the HTML file into a DOM representation
    dom = BeautifulSoup(html, 'html.parser')

    # extract the movies (using the function you implemented)
    movies = extract_movies(dom)

    save_csv("movies.csv", movies)
