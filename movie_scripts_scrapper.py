from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

#Return HTML Source Page of Url
def loadUrl(url,driver):
    driver.get(url)
    time.sleep(5)
    return driver.page_source

#Get Movie Script Text
def getMovieScript(name,source):
    contents = BeautifulSoup(source, 'html.parser')
    preText = contents.pre.get_text()
    text_file = open('./source_outputs/movies/'+name+'.txt', 'w')
    text_file.write(preText)
    text_file.close()

#Write Movie Script to CSV
def scriptParser(name):
    file = open('./source_outputs/movies/'+name+'.txt',"r+") 
    preText = file.readlines()
    scriptText = []
    sceneText = []
    sceneText.append('')
    regstr = ''
    #Regex to Parse Movie Script 
    pattern = re.compile(r'^\d.+\d\n?$|^\d+.$')
    patternB = re.compile(r'^EXT\..+$|^INT\..+$')
    patternC = re.compile(r'^I/E.+$')
    for i in range(len(preText)):
        text = preText[i]
        if pattern.search(text.strip()) != None or patternB.search(text.strip()) != None or patternC.search(text.strip()) != None:
            sceneText.append(text.strip())
            if regstr:
                scriptText.append(regstr)
                regstr = ''
        else:
            regstr = regstr +' '+ text.strip()
        
        #last Index
        if i == len(preText) -1:
            scriptText.append(regstr)
    
    #DataFrame
    df_movie = pd.DataFrame({'Scenes':sceneText,'Scripts':scriptText})
    df_movie.to_csv('./data/movies/'+name + '.csv',index=False)

# Get Array of movie names from https://www.imsdb.com
def getMovieTitles(source):
    contents = BeautifulSoup(source,'html.parser')
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
        title_url.append((tx,url))
    df = pd.DataFrame(title_url)
    #Trim unecessary
    df = df.iloc[65:1275]
    df.to_csv('./url/movies_url.csv',index=True)

#Return movie url from title
def generateMovieUrl(title):
    url = "https://www.imsdb.com/scripts/" + title+".html"
    return url

# Execute Script
if __name__ == "__main__":
    try:
        #Driver
        driver = Chrome(executable_path='./drivers/chromedriver.exe')

        #Example movie links / scripts
        ex1_url = 'https://www.imsdb.com/scripts/A-Quiet-Place.html'
        ex2_url = 'https://www.imsdb.com/scripts/Black-Panther.html'
        ex1_tl = 'A-Quiet-Place'
        ex2_tl = 'Black-Panther'
        getMovieScript(ex1_tl,loadUrl(ex1_url,driver))
        getMovieScript(ex2_tl,loadUrl(ex2_url,driver))
        scriptParser(ex1_tl)
        scriptParser(ex1_tl)

        #List of movies available on imsdb
        allMoviesUrl = "https://www.imsdb.com/all%20scripts/"

        # Load all movie names
        tl = getMovieTitles(loadUrl(allMoviesUrl,driver))
        movieTitlesToCsv(tl)

        # Get all movies scripts

        # Parse movie scripts and save to csv file

        # Close browser
    finally:
        driver.quit()