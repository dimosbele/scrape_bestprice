"""
This is the main script of the process that scrapes 'BestPrice' e-commerce site
"""

# import other scripts and classes
from bestprice import *
from general import *

# a list with a sample of the product subcategories that were scraped
# 'N' refers to the number of products that will be scraped from each subcategory
categories = [
{'Category':'Mobiles', 'SubCategory':'Mobile_phone', 'url':'https://www.bestprice.gr/cat/806/mobile-phones.html?pg={}', 'N':1600},
{'Category':'Mobiles', 'SubCategory':'Bluetooth', 'url':'https://www.bestprice.gr/cat/813/bluetooth.html?v=r&pg={}', 'N':1900},
{'Category':'Mobiles', 'SubCategory':'Handsfree', 'url':'https://www.bestprice.gr/cat/811/hands-free.html?v=r&pg={}', 'N':2400},
]

# create an object of the bestprice class
sk = bestprice()

# for each category call the 'scrape_bestprice' function to scrape the corresponding pages   
for category in categories[0:]:
	
	# define the path of the .csv file in which the scraped data will be saved
    csvFileName = '.../results/' + category['Category'] + '-' + category['SubCategory']+'.csv'
	# initialize the .csv file
    initializeCsv(filename=csvFileName)
 
    print('- Going to scrape the Subcategory - ', category['SubCategory'], ' - ', category['Category'])
    # call the function to start the scraping process
    sk.scrape_bestprice(category)
