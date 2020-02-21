from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import re

#Return Source Page of Url
def loadUrl(url):
    driver = Chrome(executable_path='./drivers/chromedriver.exe')
    WebDriverWait(driver,5)
    driver.get(url)
    result = driver.page_source
    driver.quit()
    return result

#Get Movie Source
def getMovieScript(filename,source):
    contents = BeautifulSoup(source, 'html.parser')
    preText = contents.pre.get_text()
    text_file = open('./source_outputs/'+filename+'.txt', 'w')
    text_file.write(preText)
    text_file.close()

#Write DataFrame to CSV
def scriptParser(filename):
    file = open('./source_outputs/'+filename+'.txt',"r+") 
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
    df_movie.to_csv('./data/'+filename + '.csv',index=False)

url = 'https://www.imsdb.com/scripts/A-Quiet-Place.html'
allMoviesUrl = "https://www.imsdb.com/all%20scripts/"
#getMovieScript('A-Quiet-Place',loadUrl(url))
scriptParser('A-Quiet-Place')