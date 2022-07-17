## Technical And Fundamental Analysis of Bank Of Baroda

#### Rahul Jha (210802)

## 1. Preliminaries

- Extracted P&L data and current stock price from [Moneycontrol](https://www.moneycontrol.com/financials/bankofbaroda/profit-lossVI/BOB{}#BOB) using [Beautiful soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). The assumption I made was that people who rely on fundamentals are not too concerned with day to day price fluctuations, so a static price (price as of writing) would suffice for calculating the P/E ratio and therefore the PEG metric.

- For technical analysis historical data was required and while [Yahoo! Finance](https://finance.yahoo.com/quote/BANKBARODA.NS/history?period1=1594857600&period2=1657929600&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true) provides CSV data, where is the fun in that. I used selenium to automate the scraping process, and finally saved the daily OHLC (Open, high, low, close) data in a CSV file. 

- The results (graphs et al.) are accessible [here](https://theslytherin.gitlab.io/assets/fac_demo/demo.html).

  

## 2. Technical Analysis

1. #### McGinley Indicator

   McGinley Indicator is an alternative to moving averages. Moving averages (with meaningful time periods, no one made bank using a 5 day SMA) lag behind the actual prices. Sometimes significantly. McGinley Indicator creates a trendline (trend-curve lol) using just the previous day's information, and is therefore a much better fit to the actual price chart. In my analysis also, McGinley Average was a better fit to the line graph, and on one  occasion even reversed the buy signal. 

   According to the datasheet, Bank of Baroda stock is above every Moving Average/ McGinley Average line and is therefore in the **buy** zone. 

   **According to McGinley, BOB is a good buy.**

2. #### Pretty Good Indicator:

   This indicator measures how close the closing price is to the simple moving average in terms of the true range. For example, if PGI is 0.2 and the true range (on average) is 5, then the closing price is 1 more than the moving average. 

   It is used as follows: 

   - PGI > 3 means one should go long.
   - PGI < -3 means one should go short.
   - PGI = 0 means one should exit the position

   From the datasheet hosted [here](https://theslytherin.gitlab.io/assets/fac_demo/demo.html), it is clear that the PGI has been consistently between the two thresholds. But the numbers are arbitrary. So if I modify my strategy to buy when PGI crosses 0.5, I would go long on Bank of Baroda, and this claim is also supported by the moving average chart.

   **According to PGI, BOB is a good buy**.
   
   
## 3. Fundamental Analysis

I evaluated the scrip on two metrics, Earnings Per Share and PEG (Price Earnings Growth).

1. #### Earnings Per Share

   ​	It is simply the net profit divided by the number of outstanding shares. This metric is readily available because companies disclose it in their annual financial reports. Now, the EPS of a company by itself divulges little information about the company. A company with an EPS of 5000 sounds pretty cool until you find out that it's direct competitor has an EPS of 7000. So I scraped the annual financial reports of all banks in NIFTY200 (kidding, I excluded IDFC and IDBI because they are bad banks) and plotted their EPS' on a line chart. Bank of Baroda had the third highest EPS last financial year and has consistently been in the top 5 for the last 4 years. 2018 was weird because every bank's EPS was very close to zero. 

   **Therefore, according to EPS analysis, BOB is a good buy**.

   

2. #### Price Earning Growth

   PE ratio is a widely used metric in technical analysis. It is the ratio of a scrips trading price and it's EPS. But PE ratios can be deceptive. A company with a high PE ratio may have declining earnings per share. That is why the PEG metric is used. It rewards companies with rapidly growing earnings per share. Now, BOB had a blast in FY ending 2022, with profits increasing by 8 times, therefore it has the lowest PEG among all banks in NIFTY200.

   **Solid Buy**.

   

   

   

   

   



