from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import pandas as pd
from datetime import datetime

# create class to scrape stock data
class StockScraper:
    base_day = 40909
    base_date = (2012, 1, 1)
    d0 = datetime(*base_date)

    def __init__(self, stock, c_name, c_sector):
        self.stock = stock
        self.c_name = c_name
        self.c_sector = c_sector
    
    
    def getDate(self,year, month, date):
        # get the number of days since 01 Jan 2012
        d1 = datetime(year, month, date)
        delta = d1 - self.d0
        ndate = delta.days
    
        return ndate+self.base_day
    
    def checkContent(self,url):
        # check if the url is valid
        if url == None:
            return None

        try:
            # open the url and get content
            req = Request(url=url, headers={'user-agent': 'news_scraper'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page,'html.parser')
        except:
            return None

        # get the content, which is inside the div tag with class 'artText medium'
        # print(soup.prettify())
        content = soup.find_all(class_='artText')
        # check if the content is empty
        if len(content) == 0:
            print("No content found at the url: ", url)
            return None

        # check if content contains the company name or sector
        content_txt = content[0].text
        if self.c_name in content_txt or self.c_sector in content_txt:
            return content_txt

        return None

    def getRelatedNews(self, year,month,day):
        date = (year, month, day)
        base_url = "https://economictimes.indiatimes.com"
        url = f'https://economictimes.indiatimes.com/archivelist/year-{date[0]},month-{date[1]},starttime-{self.getDate(*date)}.cms'
        print("url: ", url)
    
        request = Request(url=url, headers={'user-agent': 'news_scraper'})
        response = urlopen(request)
    
        # parse the data
        html = BeautifulSoup(response, features='html.parser')
        news_table = html.find_all(class_='content')
    
        news_list = news_table[0].find_all('li')
        print("len(news_list): ", len(news_list))
    
        news_with_cname = []
        news_with_csector = []
        # iterate over each news element
        for news_item in news_list:
            title = news_item.find('a').text
            content_url = base_url + news_item.find('a')['href']
    
            ret_content = self.checkContent(content_url)
            if ret_content != None:
                if self.c_name in ret_content:
                    news_with_cname.append((title, content_url, ret_content))
                else:
                    news_with_csector.append((title, content_url, ret_content))
        if len(news_with_cname) > 0:
            return news_with_cname
        return news_with_csector