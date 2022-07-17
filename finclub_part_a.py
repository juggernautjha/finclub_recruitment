#!/usr/bin/env python
# coding: utf-8

# Actually performing the calculations is trivial, I just have to get the data. This notebook _should_ help me do just that. My sources are moneycontrol and Yahoo! Finance. Now Yahoo! Finance is sad because it readily gives the price data in csv format. I do not _want_ to scrape, but looks like I have no other choice. 
# 

# ## Part 1
# 
# Extracting Balance Sheet from Moneycontrol and OHLC (open, high, low, close data) from Yahoo! Finance. Now moneycontrol is pesky, it does not allow me to save data in csv format,
# and because I am a lifelong linux enthusiast, I will rather die before using MS Excel. So Let me spin up a selenium
# instance. Or maybe try beautifulsoup. 
# 
# 
# Life Update: I had to use selenium and bit of arm twisting to scrape data from Yahoo! Finance because morons use a javascript routine to fetch data instead of using static pages. It is sad, I know.

# In[13]:


#all imports in one place 

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
#at this point, I am basically copy pasting from the instagram scraper I once
#wrote, so a lot of these imports might turn out to be useless.
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import matplotlib.pyplot as plt


# In[ ]:


'''

READ ONLY: You cannot really make my life more difficult Rahul, but it would be 
better if you do not execute this cell. 
'''



#uld be easy (I'll see lol), and I'll just graph it. I have no idea what to do with after that.

# ## Part 2
# This is where the actual magic (analysis) happens. None of this depends on the cells above. I mean yeah you'll need to run the cell with all the imports because that is a good practice, but please for the love of all things holy **do not** run the data collection cells. I have all the data I need.

# In[14]:


#defining stuff
DATE = 0
OPEN = 1
HIGH = 2
LOW = 3
CLOSE = 4


# In[15]:


hist = pd.read_csv('price-history_.csv')
hist
# fig2 = make_subplots(specs=[[{"secondary_y": True}]])
# fig2.add_trace(go.Scatter(x=hist['Date'],y=hist['Close'],name='Price'),secondary_y=False)
# fig2.add_trace(go.Bar(x=hist['Date'],y=hist['Volume'],name='Volume'),secondary_y=True)
# fig2.show()


# Look at the beautiful graph. It is interactive. The only drawback is that is uses javascript for reasons known to no one. Not me. Now, to calculate technical indicators, I can either write functions that take a dataframe and then add a column, or something. Or I can go full consultant and use readymade tools. Let me do both. This will allow me to check if I am truly a top comder. 

# In[16]:


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

# In[17]:


rows = []
def populate_rows(): #loops on dataframes -> bad idea *retches*
    with open('price-history_.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            z = [row[0]] + [eval(x) for x in row[1:]]
            rows.append(z)

populate_rows()


# In[18]:


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


# In[19]:


#Comparison between moving average and mc_ginley
for I in range(10, 100, 10):
    print(I)
    graph(I)
    graph_mc_ginley(rows, I/2)


# So, the mc_ginley metric (idk lol) lags a lot less than simple moving average. 
# Now. to implement PGO (or PGI, whatever floats your boat) I'll have to first implement EMA. Which should be easy.

# In[20]:


def EMA(hist, n, col):
    c = hist
    c['ewm'] = c[col].ewm(span=n,min_periods=0,adjust=False,ignore_na=False).mean()
    return c
#works splendidly, cross checked from trading view.


# In[21]:


def wwma(values, n):
    """
     J. Welles Wilder's EMA 
    """
    return values.ewm(alpha=1/n, adjust=False).mean()


# In[22]:


def ATR(df, n=14):
    data = df.copy()
    high = data['High']
    low = data['Low']
    close = data['Close']
    data['tr0'] = abs(high - low)
    data['tr1'] = abs(high - close.shift())
    data['tr2'] = abs(low - close.shift())
    tr = data[['tr0', 'tr1', 'tr2']].max(axis=1)
    atr = wwma(tr, n)
    df['atr'] = atr
    return df


# In[23]:


def PGO(n):
    c = SMA(n)
    #this gives us a dataframe with SMA. I do NOT want to code ever again.
    c = ATR(c, n)
    #this will give us a dataframe with average
    c = EMA(c, n, 'atr')
    c.dropna(inplace=True)
    c['PGO'] = (c['Close'] - c['SMA'])/c['ewm']
    return c
#works splendidly. Checked.


# Technical Indicators implemented. I have little to no idea what to do with them. Sure, I can graph them but what next? If only I knew how to trade....
# 
# Now for the _fundamental_ indicators, EPS is of no use by itself. So I'll modify the data fetching function and just extract the profit and EPS rows for banks. Then compare. Then sleep.

# In[24]:


BANKS_NIFTY_200 = {
    "AUBANK" : "https://www.moneycontrol.com/financials/ausmallfinancebank/profit-lossVI/ASF02/{}#ASF02",
    "AXISBANK" : "https://www.moneycontrol.com/financials/axisbank/profit-lossVI/AB16/{}#AB16",
    "BANDHANBANK" : "https://www.moneycontrol.com/financials/bandhanbank/profit-lossVI/BB09/{}#BB09",
    "BANKBARODA" : "https://www.moneycontrol.com/financials/bankofbaroda/profit-lossVI/BOB/{}#BOB",
    "BANKINDIA" : "https://www.moneycontrol.com/financials/bankofindia/profit-lossVI/BOI/{}#BOI",
    "CANBANK" : "https://www.moneycontrol.com/financials/canarabank/profit-lossVI/CB06/{}#CB06",
    "HDFCBANK" : "https://www.moneycontrol.com/financials/hdfcbank/profit-lossVI/HDF01/{}#HDF01",
    "ICICIBANK" : "https://www.moneycontrol.com/financials/icicibank/profit-lossVI/ICI02/{}#ICI02",
    "INDIANB" : "https://www.moneycontrol.com/financials/indianbank/profit-lossVI/IB04/{}#IB04",
    "INDUSINDBK" : "https://www.moneycontrol.com/financials/indusindbank/profit-lossVI/IIB/{}#IIB",
    "KOTAKBANK" : "https://www.moneycontrol.com/financials/kotakmahindrabank/profit-lossVI/KMB/{}#KMB",
    "PNB" : "https://www.moneycontrol.com/financials/punjabnationalbank/profit-lossVI/PNB05/{}#PNB05",
    "SBIN" : "https://www.moneycontrol.com/financials/statebankofindia/profit-lossVI/SBI/{}#SBI",
    "UNIONBANK" : "https://www.moneycontrol.com/financials/unionbankofindia/profit-lossVI/UBI01/{}#UBI01",
    "YESBANK" : "https://www.moneycontrol.com/financials/yesbank/profit-lossVI/YB/{}#YB"
}

#god did this take a lot of time lololol
#Also I missed IDFC and IDBI banks because they suck. Yes.


# Now a simple scraper that would collate all data. We just need EPS and Profits over the years. Nothing More, and certainly nothing less.

# In[25]:


def scrape(url):
    urls = ['/1', '/2', '/3']
    data = dict()
    r = requests.get(url)
    soup_ = BeautifulSoup(r.text)
    z = soup_.find_all("span", class_="span_price_wrap")
#     print(z)
    try:
        data["price"] = eval(z[0].text)
    except:
        data["price"] = "NOT"
    for i in urls:
        r = requests.get(url.format(i))
        soup = BeautifulSoup(r.text)
        z = soup.find_all('tr') #bingo we have the data. Now we just have to sanitize it.
        for i in z:
            if (i.text):
                tds = i.find_all('td')
                tds = [x.text for x in tds][:-1]
                for l in range(len(tds)):
                    try:
                        
                        tds[l] = eval(tds[l].replace(",", ""))
                    except:
                        pass
                header = tds[0]
                if "Profit & Loss" in header:
                    if(header in data):
                            data[header] += tds[1:]
                    else:
                        data[header] = tds[1:]
                if header in ["Net Profit / Loss for The Year", "Basic EPS (Rs.)", "Diluted EPS (Rs.)"]:
                    if header != '\xa0' and '' not in tds:
        #                 print(tds)
        #                 write.writerow(tds)
                        if(header in data):
                            data[header] += tds[1:]
                        else:
                            data[header] = tds[1:]
    return data
all_banks = dict()
for i in BANKS_NIFTY_200:
    all_banks[i] =  scrape(BANKS_NIFTY_200[i])
    


# In[26]:


for i in all_banks:
    print(i)
    for j in all_banks[i]:
        print(j, all_banks[i][j])
    print()


# In[27]:


PE_ratio = {i : all_banks[i]['price']/all_banks[i]['Basic EPS (Rs.)'][0] for i in all_banks} #slick, innit?
EARNINGS_GROWTH = {i : (all_banks[i]['Basic EPS (Rs.)'][0] - all_banks[i]['Basic EPS (Rs.)'][1])/(all_banks[i]['Basic EPS (Rs.)'][1]) for i in all_banks}
EARNINGS_GROWTH = {i: EARNINGS_GROWTH[i]*100 for i in EARNINGS_GROWTH}
EPG = {i: PE_ratio[i]/EARNINGS_GROWTH[i] for i in PE_ratio}
PEG = {}
for i in EPG:
    if EPG[i] >= 0:
        PEG[i] = EPG[i] #because negative values are absurd

        
PE_R = {}
for i in PE_ratio:
    if PE_ratio[i] >= 0: #negative values absurd again. Loss making companies deserve love too.
        PE_R[i] = PE_ratio[i]
plt.plot([i for i in PEG], [PEG[i] for i in PEG])
plt.xticks(rotation=45, ha='right')
plt.title("PEG Ratio for Banking Scrips")
plt.show()

plt.plot([i for i in PE_R], [PE_R[i] for i in PE_R])
plt.xticks(rotation = 45, ha = 'right')
plt.title("P/E Ratio for Banking Scrips")
plt.show()
#BOB the most undervalued. Like Myself.

