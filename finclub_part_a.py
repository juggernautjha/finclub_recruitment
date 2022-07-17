#!/usr/bin/env python
# coding: utf-8

# Actually performing the calculations is trivial, I just have to get the data. This notebook _should_ help me do just that. My sources are moneycontrol and Yahoo! Finance. Now Yahoo! Finance is sad because it readily gives the price data in csv format. I do not _want_ to scrape, but looks like I have no other choice. 
# 

# ## Part 1
# 
# Extracting Balance Sheet, from Moneycontrol. Now moneycontrol is pesky, it does not allow me to save data in csv format,
# and because I am a lifelong linux enthusiast, I will rather die before using MS Excel. So Let me spin up a selenium
# instance. Or maybe try beautifulsoup.

# In[54]:


'''

READ ONLY: You cannot really make my life more difficult Rahul, but it would be 
better if you do not execute this cell. 
'''


from bs4 import BeautifulSoup
import requests
import csv

# file = open("profit_and_loss_BOB.csv", "w", newline='\n')
# urls = ['/1', '/2', '/3']
# data = dict()
# write = csv.writer(file)
# # headers = ['Interest / Discount on Advances / Bills', 'Income from Investments', 'Interest on Balance with RBI and Other Inter-Bank funds'] #trial, will extract these as well inshallah
# for i in urls:
#     r = requests.get('https://www.moneycontrol.com/financials/bankofbaroda/profit-lossVI/BOB{}#BOB'.format(i))
#     soup = BeautifulSoup(r.text)
#     z = soup.find_all('tr') #bingo we have the data. Now we just have to sanitize it.
#     for i in z:
#         if (i.text):
#             tds = i.find_all('td')
#             tds = [x.text for x in tds][:-1]
#             header = tds[0]
#             if header != '\xa0' and '' not in tds:
# #                 print(tds)
# #                 write.writerow(tds)
#                 if(header in data):
#                     data[header] += tds[1:]
#                 else:
#                     data[header] = tds[1:]
# for i in data:
#     j = [i] + data[i]
#     write.writerow([i] + data[i])


# Bingo! That was easy. Now I don't really have to save the dictionary and then go through the excruciating process of parsing JSONs everytime. Also, I guess I have enough data to do **fundamental** analysis now lol. 
# 
# 
# Life update: I ended up saving the data in a csv file because I wanted to look at the beautiful excel sheet I created.

# In[59]:


# r = requests.get('https://finance.yahoo.com/quote/BANKBARODA.NS/history')
# print(r.text)


# # Okay, so Yahoo finance does not allow scraping, that's just sad. But nothing has ever deterred the greatest of the great, Rahul Jha. They don't call me Stalker Supreme for nothing. Time to call the cavalry.

# # In[129]:


# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

# #at this point, I am basically copy pasting from the instagram scraper I once
# #wrote, so a lot of these imports might turn out to be useless.


# options = webdriver.ChromeOptions()
# s = Service('/home/juggernautjha/Rahul/vision/Selenium/chromedriver')
# driver = webdriver.Chrome(service = s, options = options)
# driver.get('https://finance.yahoo.com/quote/BANKBARODA.NS/history?period1=1594857600&period2=1657929600&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true')
# # last_height = driver.execute_script("return document.body.scrollHeight")
# # while True:
# #     # Scroll down to the bottom.
# #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# #     # Wait to load the page.
# #     time.sleep(2)
# #     print("scrolling\n")
# #     # Calculate new scroll height and compare with last scroll height.
# #     new_height = driver.execute_script("return document.body.scrollHeight")

# #     if new_height == last_height:

# #         break

# #     last_height = new_height
# import time
# time.sleep(15)
# import csv
# file = open("price-history_.csv", "w")
# write = csv.writer(file)
# write.writerow(['Date', 'Open', 'High', 'Low', 'Close', 'Adj. Close', 'Volume'])
# z = driver.find_elements(By.CSS_SELECTOR, "tr")
# for i in z[-1::-1]:
#     f = i.text.split(" ")
#     try:
#         eval(f[2])
#         f = [f[0] + " " + f[1] + " " + f[2]] + f[3:]
#     except:
#         pass
#     print(f)
#     print(len(f))
#     write.writerow(f)
#     print("written")
        
# # print("Now exporting")
# # with open("yahoo-finance-cached.html", 'w') as f:
# #     f.write(driver.page_source)


# # And we are done. Now that I have the page source, i do not need to torture my RAM and use selenium for scraping. Beautifulsoup would do just fine. Also, for the love of god and everything that is holy **DO NOT RUN** the cell above on anything with less than a few gigabytes of RAM.

# # Now I have no idea what to do with EPS and PEG. I mean sure, I can calculate it but what next? I think the way to go is to scrape data for _every_ stock in NIFTY200 (not everything, just the PE ratio and the EPS) and then compare them. Hopefully my bank will come out on top. 
# # Calculating the technical indicators should be easy (I'll see lol), and I'll just graph it. I have no idea what to do with after that.

# # In[99]:


#defining stuff
DATE = 0
OPEN = 1
HIGH = 2
LOW = 3
CLOSE = 4


# In[175]:


import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
hist = pd.read_csv('price-history_.csv')
hist
# fig2 = make_subplots(specs=[[{"secondary_y": True}]])
# fig2.add_trace(go.Scatter(x=hist['Date'],y=hist['Close'],name='Price'),secondary_y=False)
# fig2.add_trace(go.Bar(x=hist['Date'],y=hist['Volume'],name='Volume'),secondary_y=True)
# fig2.show()


# Look at the beautiful graph. It is interactive. The only drawback is that is uses javascript for reasons known to no one. Not me. Now, to calculate technical indicators, I can either write functions that take a dataframe and then add a column, or something. Or I can go full consultant and use readymade tools. Let me do both. This will allow me to check if I am truly a top comder. 

# In[186]:


#Now,n day averages aren't defined for n-1 days. Yup. Pandas for the win
def SMA(n):
    close = hist
    close['SMA'.format(n)] = close['Close'].rolling(n).mean()
    close.dropna(inplace = True)
    close.head()
    return close
c = SMA(10)

def graph(n):
    c = SMA(n)
    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3.add_trace(go.Scatter(x=c['Date'],y=c['Close'],name='Price'),secondary_y=False)
    fig3.add_trace(go.Scatter(x=c['Date'],y=c['SMA'],name='Moving Average'),secondary_y=False)
#     fig3.add_trace(go.Bar(x=hist['Date'],y=hist['Volume'],name='Volume'),secondary_y=True)
    fig3.show()
    


# N-day average works splendidly. Great Success. 
# 
# McGinley Dynamic, on the other hand, is a uniquely strange problem. I am unable to figure out what M_{t-1} should be for t = 1. I mean if I set M_1 = Close, let us see what we get.

# In[166]:


rows = []
def populate_rows(): #loops on dataframes -> bad idea *retches*
    with open('price-history_.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            z = [row[0]] + [eval(x) for x in row[1:]]
            rows.append(z)

populate_rows()


# In[196]:


def mc_ginley(rows, N):
    mc_indices = [rows[0][CLOSE]]
    for i in rows[1:]:
        prev = mc_indices[-1]
        mc_index = prev + (i[CLOSE] - prev)/(0.6* N*((i[CLOSE]/prev)**4))
        mc_indices.append(mc_index)
    return mc_indices


def graph_mc_ginley(rows, N):
    hist = pd.read_csv("price-history_.csv")
    hist['mc'] = mc_ginley(rows, N)
    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3.add_trace(go.Scatter(x=hist['Date'],y=hist['Close'],name='Price'),secondary_y=False)
    fig3.add_trace(go.Scatter(x=hist['Date'],y=hist['mc'],name='McGinley'),secondary_y=False)
    #     fig3.add_trace(go.Bar(x=hist['Date'],y=hist['Volume'],name='Volume'),secondary_y=True)
    fig3.show()


# In[197]:


#Comparison between moving average and mc_ginley
for I in range(10, 100, 10):
    print(I)
    graph(I)
    graph_mc_ginley(rows, I/2)

