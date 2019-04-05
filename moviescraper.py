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
import matplotlib.pyplot as plt

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
    allinfo = []

    for title in dom.findAll("div", {"class": "lister-item mode-advanced"}):
        infolist = []
        infolist.append(title.h3.a.text)
        for rating in title.findAll("span", {"class": "value"}):
            infolist.append(float(rating.text))
        for year in title.findAll("span", {"class": "lister-item-year text-muted unbold"}):
            year = year.text
            year = year.replace('(', '').replace(')', '').replace('II', '')\
                        .replace('I', '')
            year = int(year)
            infolist.append(year)
        for actors in title.select('a[href*=_st]'):
            infolist.append(actors.text)
        for runtime in title.findAll("span", {"class": "runtime"}):
            infolist.append(runtime.text)
        allinfo.append(infolist)

    year = []
    rating = []
    average = {}

    for row in allinfo:
        rating.append(row[1])
        year.append(row[2])
        if row[2] not in average:
            average[row[2]] = rating
        else:
            average[row[2]].append(rating)
    print(average)




    # the histogram of the data
    plt.bar(year,rating ,facecolor='g')
    plt.xlabel('years')
    plt.ylabel('ratings')
    plt.title('Ratings of movies')
    plt.axis([ 2007, 2017,7.9, 9.5])
    plt.grid(True)
    plt.show()

    # ADD YOUR CODE HERE TO EXTRACT THE ABOVE INFORMATION ABOUT THE
    # HIGHEST RATED MOVIES
    # NOTE: FOR THIS EXERCISE YOU ARE ALLOWED (BUT NOT REQUIRED) TO IGNORE
    # UNICODE CHARACTERS AND SIMPLY LEAVE THEM OUT OF THE OUTPUT.

    return allinfo   # REPLACE THIS LINE AS WELL IF APPROPRIATE

# def Average(lst):
#     return sum(lst) / len(lst)

def save_csv(outfile, movies):
    """
    Output a CSV file containing highest rated movies.
    """

    writer = csv.writer(outfile)
    writer.writerow(['Title', 'Rating', 'Year', 'Actors', 'Runtime'])
    for line in movies:
        writer.writerow(line)

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
    with open(OUTPUT_CSV, 'w', newline='') as output_file:
        save_csv(output_file, movies)
