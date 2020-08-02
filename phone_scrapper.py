from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import numpy
import requests

cat = ["Technology","Announced", "Status", "Price"]

def loadContents(url):
    time.sleep(100)
    response = requests.get(url)
    content = response.content
    return BeautifulSoup(content, 'html.parser')

def brands():
    url = "https://www.gsmarena.com/makers.php3"
    contents = loadContents(url)
    return [link.get('href') for link in contents.table.find_all('a')]

def phonesEachBrand(brand_url):
    contents = loadContents(brand_url)
    return [link.get('href') for link in contents.find('div',id='review-body').find_all('a')]

def phoneContents(phone_url):
    contents = loadContents(phone_url)
    tables = contents.find_all('table')
    network = tables[0].get_text().splitlines()
    launch = tables[1].get_text().splitlines()
    price = tables[len(tables)-2].get_text().splitlines()
    result = {"Link":phone_url,
              "Network":parsePhoneContents(network,cat[0]),
              "Announced": parsePhoneContents(launch,cat[1]),
              "Status":parsePhoneContents(launch,cat[2]),
              "Price":parsePhoneContents(price,cat[3])
             }
    return result
        
def parsePhoneContents(arr_string,c):
    index=arr_string.index(c)
    return arr_string[index+1]
    
if __name__ == "__main__":
    home_link = "https://www.gsmarena.com/"
    result = []
    for brand_link in brands():
        for phone_link in phonesEachBrand(home_link+brand_link):
            result.append(phoneContents(home_link+phone_link))
    df = pd.DataFrame(result)
    df.to_csv("phones.csv", index=False)
