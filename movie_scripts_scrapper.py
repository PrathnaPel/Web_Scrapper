from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import numpy
import requests

# Return HTML Source Page of Url


def loadUrl(url, driver):
    driver.get(url)
    time.sleep(10)
    return driver.page_source

# Get Movie Script Text


def getMovieScript(name, link):
    response = requests.get(link)
    content = response.content
    contents = BeautifulSoup(content, 'html.parser')
    preText = contents.pre.get_text()
    text_file = open('./raw/'+name+'.txt', 'w')
    text_file.write(preText)
    text_file.close()

# Write Movie Script to CSV


def scriptParser(name):
    file = open('./raw/'+name+'.txt', 'r')
    preText = file.readlines()
    file.close()
    scriptText = []
    sceneText = []
    sceneText.append('')
    regstr = ''
    # Regex to Parse Movie Script
    pattern = re.compile(
        r'^\d.*\d[a-zA-Z0-9]*\n?$|^\d+\s?.$', flags=re.MULTILINE)
    patternB = re.compile(r'^\bEXT\b.+$|^\bINT\b.+$', flags=re.MULTILINE)
    patternC = re.compile(r'^\bI/E\b.+$', flags=re.MULTILINE)
    for i in range(len(preText)):
        text = preText[i]
        if pattern.match(text.strip()) != None or patternB.match(text.strip()) != None or patternC.match(text.strip()) != None:
            sceneText.append(text.strip())
            if regstr:
                scriptText.append(regstr)
                regstr = ''
        else:
            regstr = regstr + ' ' + text.strip()

        # last Index
        if i == len(preText) - 1:
            scriptText.append(regstr)
    df_movie = pd.DataFrame({'Scenes': sceneText, 'Scripts': scriptText})
    df_movie.to_csv('./movie_scripts_data/'+name + '.csv', index=False)

# Get Array of movie names from https://www.imsdb.com


def getMovieTitles(link):
    response = requests.get(link)
    content = response.content
    contents = BeautifulSoup(content, 'html.parser')
    preText = contents.findAll('a')
    title = []
    for tx in preText:
        title.append(str(tx.get('title')).strip('Script').strip())
    return title

# Write Movie title to csv


def movieTitlesToCsv(arr):
    title_url = []
    for tx in arr:
        tx = str(tx).replace(" ", "-")
        url = generateMovieUrl(tx)
        title_url.append((tx, url))
    df = pd.DataFrame(title_url)
    # Trim unecessary
    df = df.iloc[67:df.shape[0]-7]
    df.to_csv('./url/movies_url.csv', index=False)

# Return movie url from title


def generateMovieUrl(title):
    url = "https://www.imsdb.com/scripts/" + title+".html"
    return url


# Execute Script
def executeScritp():
    # Example movie links / scripts
    ex1_url = 'https://www.imsdb.com/scripts/A-Quiet-Place.html'
    ex2_url = 'https://www.imsdb.com/scripts/Black-Panther.html'
    ex1_tl = 'A-Quiet-Place'
    ex2_tl = 'Black-Panther'
    getMovieScript(ex1_tl, ex1_url)
    getMovieScript(ex2_tl, ex2_url)
    #scriptParser(ex1_tl)
    #scriptParser(ex2_tl)
    # List of movies available on imsdb
    allMoviesUrl = "https://www.imsdb.com/all%20scripts/"

    # Load all movie names To run it you need create folder named "url"
    #tl = getMovieTitles(allMoviesUrl)
    # movieTitlesToCsv(tl)

    # Get all movies scripts

    # Parse movie scripts and save to csv file

    # Close browser