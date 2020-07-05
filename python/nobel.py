import requests

response = requests.get('https://en.wikipedia.org/wiki/Nobel_Prize')

response # output: <Response [200]>

dir(response) # output: a response objektum attribútumjai

response.headers

response.text

response = requests.get('http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/nama_10_gdp?geo=EU28&precision=1&na_item=B1GQ&unit=CP_MEUR&time=2018&time=2019')

response # output: <Response [200]>

response.json()

""" 
output: 

{'version': '2.0',
 'label': 'GDP and main components (output, expenditure and income)',
 'href': 'http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/nama_10_gdp?geo=EU28&precision=1&na_item=B1GQ&unit=CP_MEUR&time=2018&time=2019',
 'source': 'Eurostat',
 'updated': '2020-07-01',
 'extension': {'datasetId': 'nama_10_gdp',
  'lang': 'EN',
  'description': None,
  'subTitle': None},
 'class': 'dataset',
 'value': {'0': 15915732.9, '1': 16452065.5},
 'dimension': {'unit': {'label': 'unit',
   'category': {'index': {'CP_MEUR': 0},
    'label': {'CP_MEUR': 'Current prices, million euro'}}},
  'na_item': {'label': 'na_item',
   'category': {'index': {'B1GQ': 0},
    'label': {'B1GQ': 'Gross domestic product at market prices'}}},
  'geo': {'label': 'geo',
   'category': {'index': {'EU28': 0},
    'label': {'EU28': 'European Union - 28 countries (2013-2020)'}}},
  'time': {'label': 'time',
   'category': {'index': {'2018': 0, '2019': 1},
    'label': {'2018': '2018', '2019': '2019'}}}},
 'id': ['unit', 'na_item', 'geo', 'time'],
 'size': [1, 1, 1, 2]}
"""