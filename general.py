"""
This is the script with the functions that are used from 'bestprice.py' file
"""
# import libraries
import csv
import random
from collections import OrderedDict
from openpyxl.styles import PatternFill
from itertools import cycle
import traceback
import requests
from bs4 import BeautifulSoup
import pandas as pd


#gives different user agent randomly for each request.
agent_version = '%.2f' % (random.randint(20, 100) + random.randint(1, 100)/float(100))
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 8\.0; Windows NT 5\.1; SV1)  Chrome/%s.2924.87 Safari/537.36' % agent_version
}


def get_free_proxies(url, anonymity):
	# scrapes the site with the free proxies
	
	# perform the page request
    page = requests.get(url)
	# convert the page to a BeautifulSoup object
    soup = BeautifulSoup(page.content, 'html.parser')
	
	# find the html tags with the free proxies
    table = soup.find('table', id='proxylisttable')
    table_body = table.find("tbody")
    trs = table_body.find_all("tr")
	
	# create a list to store the proxies
    proxies = []
	# extract the details of each proxy from the corresponding html tags
    for tr in trs[0:]:
        tds = tr.find_all("td")
        if tds[4].text.strip() in anonymity:    
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            proxy = ip+':'+port
			# append the proxy to the list
            proxies.append(proxy)
			
	# return the list of proxies
    return proxies

def update_proxy_pool(site):
	# select one of the two sites and scrape the available free proxies
    print('Updating proxy_pool...')
    if site==1:
        print('Site No. 1')
        url = 'https://free-proxy-list.net/'
    else:
        print('Site No. 2')
        url = 'https://www.sslproxies.org/'
	
	# call the function to scrape the selected site
    proxies = get_free_proxies(url, 'elite proxy')
	
	# convert the list to cycle
    proxy_pool = cycle(proxies)
    
	# return the proxies
    return proxy_pool


def initializeCsv(filename=''):
	# creates a .csv filename with the needed column names
	
	# create a dictionary with the needed .csv columns
    dataFormat = OrderedDict()
    dataFormat['Category']= ''
    dataFormat['SubCategory']= ''
    dataFormat['url']= ''
    dataFormat['N']= ''
    dataFormat['Title']= ''
    dataFormat['Price']= ''
    dataFormat['Description']= ''
    dataFormat['Page']= ''
    dataFormat['brand_name']= ''
    dataFormat['brand_url']= ''

	# create and save the .csv file
    keys = dataFormat.keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.writer(output_file)
        dict_writer.writerow(keys)

def appendDictToCsv(filename='', data={}):
	# writes a python dictionary to a .csv file
	
    keys = data.keys()
    with open(filename, 'a', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writerow(data)
        
        