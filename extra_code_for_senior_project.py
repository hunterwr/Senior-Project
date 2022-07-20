#create annual income statements
  annual_is_stats = []
  for s in annual_is:
    statement = {}
    for key, val in s.items():
      try:
        statement[key] = val['raw']
      except TypeError:
        continue
      except KeyError:
        continue
    annual_is_stats.append(statement)

  #create quarterly income statements
  quarterly_is_stats = []
  for s in quarterly_is:
    statement = {}
    for key, val in s.items():
      try:
        statement[key] = val['raw']
      except TypeError:
        continue
      except KeyError:
        continue
    quarterly_is_stats.append(statement)

  #create annual income statements
  annual_cf_stats = []
  for s in annual_cf:
    statement = {}
    for key, val in s.items():
      try:
        statement[key] = val['raw']
      except TypeError:
        continue
      except KeyError:
        continue
    annual_cf_stats.append(statement)

  #create quarterly income statements
  quarterly_cf_stats = []
  for s in quarterly_cf:
    statement = {}
    for key, val in s.items():
      try:
        statement[key] = val['raw']
      except TypeError:
        continue
      except KeyError:
        continue
    quarterly_cf_stats.append(statement)

  #create annual income statements
  annual_bs_stats = []
  for s in annual_bs:
    statement = {}
    for key, val in s.items():
      try:
        statement[key] = val['raw']
      except TypeError:
        continue
      except KeyError:
        continue
    annual_bs_stats.append(statement)

  #create quarterly income statements
  quarterly_bs_stats = []
  for s in quarterly_bs:
    statement = {}
    for key, val in s.items():
      try:
        statement[key] = val['raw']
      except TypeError:
        continue
      except KeyError:
        continue
    quarterly_bs_stats.append(statement)



    ticker='GRBK'

#Create the urls
url_statistics = f'https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}'
url_financials = f'https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}'
url_historical = f'https://finance.yahoo.com/quote/{ticker}/history?p={ticker}'


driver.get(url_financials)
time.sleep(3)

#button = driver.find_elements_by_xpath("//*[@id="Col1-1-Financials-Proxy"]/section/div[1]/div[2]/button/div")
#'//div[@class="css-ais6tt"]//button[3]'
#//*[@id="Col1-1-Financials-Proxy"]/section/div[1]/div[2]/button/div/span

# button = driver.find_element_by_xpath('//*[@id="Col1-1-Financials-Proxy"]/section/div[1]/div[2]/button/div/span')
# button.click()
# time.sleep(0.5)

soup = BeautifulSoup(driver.page_source, 'html.parser')

pattern = re.compile(r'\s--\sData\s--\s')
script_data = soup.find('script', text=pattern).contents[0]

start = script_data.find("context")-2
end = script_data.find("root.YAHOO ||")-2

#data = [json.loads(line) for line in open('extra.json','r')]
  
json_data = json.loads(script_data[start:end])

keys = json_data['context']['dispatcher']['stores']['QuoteTimeSeriesStore']['timeSeries'].keys()

#loop through all the keys in the timeSeries store
for key in keys:
    #the keys are broken into two categories, annual and trailing (twelve months)
    if (key[:6] =='annual'):
        #copy the json data for the key
        temp_json = json_data['context']['dispatcher']['stores']['QuoteTimeSeriesStore']['timeSeries'][key]
        check_data = pd.json_normalize(temp_json)
        if (not check_data.empty):
            if (check_data['asOfDate'].isnull().values.any()):
                print('skipped ' + key)
            else:
                collected_data = check_data['asOfDate']
                print('found a full date column')
        else:
            pass
    else:
        print('skipped ' + key)

#loop through all the keys in the timeSeries store
for key in keys:
    #the keys are broken into two categories, annual and trailing (twelve months)
    if (key[:6] =='annual'):
        #copy the json data for the key
        temp_json = json_data['context']['dispatcher']['stores']['QuoteTimeSeriesStore']['timeSeries'][key]
        temp_data = pd.json_normalize(temp_json)
        #replace the generic value column name with the key name
        if (not temp_data.empty):
            temp_data = temp_data.rename(columns={'reportedValue.raw': key})
            temp_data = temp_data[key]
            print(f'about to merge ' + key + ' table')
            collected_data = pd.merge(collected_data, temp_data, left_index=True, right_index=True)
            print(f'succesfully added ' + key + ' table to the collection.')
        else:
            pass
        
    else:
        print('skipped ' + key)
collected_data['ticker'] = ticker
display(collected_data)





ticker='AAPL'

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

# pizzaJson = [json.loads(full) for full in open('sample.json','r')]
# print(pizzaJson)
# print(type(pizzaJson))
start = script_data.find("context")-2
end = script_data.find("root.YAHOO ||")-2
#print(script_data[start:end])

json_data = json.loads(script_data[start:end])

json_data['context'].keys()

#annual_is = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory']['incomeStatementHistory']
# quarterly_is = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistoryQuarterly']['incomeStatementHistory']

# annual_cf = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistory']['cashflowStatements']
# quarterly_cf = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistoryQuarterly']['cashflowStatements']

# annual_bs = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistory']['balanceSheetStatements']
# quarterly_bs = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistoryQuarterly']['balanceSheetStatements']