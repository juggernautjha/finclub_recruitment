from bs4 import BeautifulSoup
import requests
import csv
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import matplotlib.pyplot as plt




'''This is pretty trashy, just scrapes P&L data off moneycontrok'''
file = open("profit_and_loss_BOB.csv", "w", newline='\n')
urls = ['/1', '/2', '/3']
data = dict()
write = csv.writer(file)
# headers = ['Interest / Discount on Advances / Bills', 'Income from Investments', 'Interest on Balance with RBI and Other Inter-Bank funds'] #trial, will extract these as well inshallah
for i in urls:
    r = requests.get('https://www.moneycontrol.com/financials/bankofbaroda/profit-lossVI/BOB{}#BOB'.format(i))
    soup = BeautifulSoup(r.text)
    z = soup.find_all('tr') #bingo we have the data. Now we just have to sanitize it.
    for i in z:
        if (i.text):
            tds = i.find_all('td')
            tds = [x.text for x in tds][:-1]
            header = tds[0]
            if header != '\xa0' and '' not in tds:
#                 print(tds)
#                 write.writerow(tds)
                if(header in data):
                    data[header] += tds[1:]
                else:
                    data[header] = tds[1:]
for i in data:
    j = [i] + data[i]
    write.writerow([i] + data[i])


# Bingo! That was easy. Now I don't really have to save the dictionary and then go through the excruciating process of parsing JSONs everytime. Also, I guess I have enough data to do **fundamental** analysis now lol. 
# 
# 
# Life update: I ended up saving the data in a csv file because I wanted to look at the beautiful excel sheet I created.

# Okay, so Yahoo finance does not allow scraping, that's just sad. But nothing has ever deterred the greatest of the great, Rahul Jha. They don't call me Stalker Supreme for nothing. Time to call the cavalry.
options = webdriver.ChromeOptions()
s = Service('/home/juggernautjha/Rahul/vision/Selenium/chromedriver')
driver = webdriver.Chrome(service = s, options = options)
driver.get('https://finance.yahoo.com/quote/BANKBARODA.NS/history?period1=1594857600&period2=1657929600&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true')
# last_height = driver.execute_script("return document.body.scrollHeight")
# while True:
#     # Scroll down to the bottom.
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#     # Wait to load the page.
#     time.sleep(2)
#     print("scrolling\n")
#     # Calculate new scroll height and compare with last scroll height.
#     new_height = driver.execute_script("return document.body.scrollHeight")

#     if new_height == last_height:

#         break

#     last_height = new_height
import time
time.sleep(15)
import csv
file = open("price-history_.csv", "w")
write = csv.writer(file)
write.writerow(['Date', 'Open', 'High', 'Low', 'Close', 'Adj. Close', 'Volume'])
z = driver.find_elements(By.CSS_SELECTOR, "tr")
for i in z[-1::-1]:
    f = i.text.split(" ")
    try:
        eval(f[2])
        f = [f[0] + " " + f[1] + " " + f[2]] + f[3:]
    except:
        pass
    print(f)
    print(len(f))
    write.writerow(f)
    print("written")
        
# print("Now exporting")
# with open("yahoo-finance-cached.html", 'w') as f:
#     f.write(driver.page_source)


# And we are done. Now that I have the page source, i do not need to torture my RAM and use selenium for scraping. Beautifulsoup would do just fine. Also, for the love of god and everything that is holy **DO NOT RUN** the cell above on anything with less than a few gigabytes of RAM.

# Now I have no idea what to do with EPS and PEG. I mean sure, I can calculate it but what next? I think the way to go is to scrape data for _every_ stock in NIFTY200 (not everything, just the PE ratio and the EPS) and then compare them. Hopefully my bank will come out on top. 
# Calculating the technical indicators sho
