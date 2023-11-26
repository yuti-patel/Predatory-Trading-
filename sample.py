# import stockScraper.py and use it to scrape stock data
from stockScraper import StockScraper as ss
import pandas as pd

stock = 'NMDC.NS'
c_name = 'NMDC'
c_sector = 'Mining'
scraper = ss(stock, c_name, c_sector)

drop_day = scraper.getRelatedNews(2021,7,9)
print("len(drop_day): ", len(drop_day))
if len(drop_day) > 0:
    print(drop_day[0])

recov_day = scraper.getRelatedNews(2021,7,16)
print("len(recov_day): ", len(recov_day))
if len(recov_day) > 0:
    print(recov_day[0])
