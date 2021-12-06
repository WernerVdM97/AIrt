"""
This file contains a script that scrapes the wikiart database for a certain specified amount of photos for given genres.
The amount of images downloaded can be controlled in the genres dictionary.
This method is up-to-date with respect to url names and image amounts as of June 2017.
"""

import os
import urllib
import requests
import itertools
import multiprocessing
import re
from multiprocessing import Pool
from bs4 import BeautifulSoup
from pathlib import Path

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings

original_images_dir = Path(settings.ORIGINAL_IMAGES_PATH)

# A list of genres hosted on wikiart.org as well as the number of pages to pull images from, numbers were set from manual inspection and are only approximations of how many pages each genre contains
genres = [
    ("portrait", 250),
    ("landscape", 250),
    ("genre-painting", 250),
    ("abstract", 250),
    ("religious-painting", 140),
    ("cityscape", 110),
    ("figurative", 75),
    ("still-life", 50),
    ("symbolic-painting", 50),
    ("nude-painting-nu", 50),
    ("mythological-painting", 35),
    ("marina", 30),
    ("flower-painting", 30),
    ("animal-painting", 30),
]


# Access the html of the page given a genre and pagenumber that are used to generate a url, from this html find the urls of all images hosted on the page using page layout as of June 2017, return a list of alls urls to paintings
def soupit(j, genre):
    try:
        url = "https://www.wikiart.org/en/paintings-by-genre/" + genre + "/" + str(j)
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        urls = []

        container = soup.select_one("div.artworks-by-dictionary")
        art_dict = container["ng-init"]

        url_regex = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        urls = re.findall(url_regex, art_dict)

        print(str(genre) + " images found: " + str(len(urls)))
        return urls
    except Exception as e:
        print("soupit exception: " + e)
        print("Failed to find the following genre page combo: " + genre + str(j))


# Given a url for an image, we download and save the image while also recovering information about the painting in the saved name depending on the length of the file.split('/') information (which corresponds to how much information is available)
def dwnld(web, genre):
    i, file = web
    name = file.split("/")
    savename = ""
    if len(name) == 6:
        savename = Path.joinpath(
            original_images_dir, genre, name[4] + "+" + name[5].split(".")[0] + ".jpg"
        )
    if len(name) == 5:
        savename = Path.joinpath(
            original_images_dir, genre, name[4].split(".")[0] + ".jpg"
        )
    if len(name) == 7:
        savename = Path.joinpath(
            original_images_dir, genre, name[5] + "+" + name[6].split(".")[0] + ".jpg"
        )

    print("dwnld " + genre + str(i))
    # If we get an exception in this operation it is probably because there was a nonstandard unicode character in the name of the painting, do some fancy magic to fix this in the exception handling code
    try:
        urllib.request.urlretrieve(file, savename)
    except Exception:
        file = urllib.parse.urlsplit(file)
        file = list(file)
        file[2] = urllib.parse.quote(file[2])
        file = urllib.parse.urlunsplit(file)
        try:
            urllib.request.urlretrieve(file, savename)
            print("Suceeded on second try for " + file)
        except Exception:
            print("We failed on the second try for " + file)


# We can run both the url retrieving code and the image downloading code in parallel, and we set up the logic for that here
def for_genre(genre, num):
    cpu_count = multiprocessing.cpu_count() - 1
    with Pool(processes=cpu_count) as pool:
        nums = list(range(1, num))
        results = pool.starmap(soupit, zip(nums, itertools.repeat(genre)))
        pool.close()
        pool.join()

    # build up the list of urls with the results of all the sub-processes that succeeded in a single list
    new_results = []
    for j in results:
        if j:
            for i in j:
                new_results.append(i)

    with Pool(processes=cpu_count) as download_pool:
        download_pool.starmap(
            dwnld, zip(enumerate(new_results), itertools.repeat(genre))
        )
        download_pool.close()
        download_pool.join()


if __name__ == "__main__":
    original_images_dir.mkdir(parents=True, exist_ok=True)
    for (g, n) in genres:
        Path.joinpath(original_images_dir, g).mkdir(parents=True, exist_ok=True)
        for_genre(g, n)

