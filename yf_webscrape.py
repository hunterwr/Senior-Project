import re
import json
import csv
import time

from IPython.display import display
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import requests
from requests_html import HTMLSession

from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions



def scrape(ticker):
  "This opens the edge driver with on a given url"
  #Create the urls
  url_statistics = f'https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}'
  url_financials = f'https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}'
  url_historical = f'https://finance.yahoo.com/quote/{ticker}/history?p={ticker}'


  driver.get(url_financials)
  time.sleep(3)

  soup = BeautifulSoup(driver.page_source, 'html.parser')

  pattern = re.compile(r'\s--\sData\s--\s')
  script_data = soup.find('script', text=pattern).contents[0]

  start = script_data.find("context")-2

  json_data = json.loads(script_data[start:-12])

  json_data['context'].keys()

  annual_is = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory']['incomeStatementHistory']
  quarterly_is = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistoryQuarterly']['incomeStatementHistory']

  annual_cf = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistory']['cashflowStatements']
  quarterly_cf = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistoryQuarterly']['cashflowStatements']

  annual_bs = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistory']['balanceSheetStatements']
  quarterly_bs = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistoryQuarterly']['balanceSheetStatements']

  qis = pd.json_normalize(quarterly_is)
  qis['ticker'] = ticker
  qcf = pd.json_normalize(quarterly_cf)
  qcf['ticker'] = ticker
  qbs = pd.json_normalize(quarterly_bs)
  qbs['ticker'] = ticker

  result = pd.merge(qis, qcf, on=["ticker", "endDate.raw"])

  end_result = pd.merge(result, qbs, on=["ticker", "endDate.raw"])

  return end_result

def remove_fluff(df):
    for col_name in df.columns:
        if (col_name[-8:]  == '.longFmt' or col_name[-4:] == '.fmt'):
          del df[col_name]


#Initialize the driver
options = EdgeOptions()
options.use_chromium = True
driver = Edge(options=options)

url = 'https://finance.yahoo.com/'

driver.get(url)

grbk = scrape('GRBK')

grbk.info()

for col_name in grbk.columns:
    print(col_name)


pd.display(grbk_clean)

# ais = pd.json_normalize(annual_is)
# ais.info()


# table = pd.json_normalize(rev_estimates)

# data = table.filter(['earnings.earningsAverage.raw', 'earnings.earningsLow.raw', 'earnings.earningsHigh.raw', 'earnings.revenueAverage.raw', 'earnings.revenueLow.raw', 'earnings.revenueHigh.raw'],axis=1)

# data['ticker'] = ticker


















