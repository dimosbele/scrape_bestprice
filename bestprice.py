"""
This is the script with the class and the functions that are used to scrape 'BestPrice' e-commerce site
"""

# import 'general' script
from general import *

# import libraries
import requests
from bs4 import BeautifulSoup
import re
from collections import OrderedDict
from itertools import cycle
import traceback
from datetime import datetime

# set counters 
cnt_pages = 0
cnt_error = 0
# call 'update_proxy_pool' function in order to get a list of proxies
proxy_pool = update_proxy_pool(1)
# set the site that will be scraped in order to gather new proxies later
n_site = 0

class bestprice:
	# the class that is used to scrape the 'BestPrice' e-commerce site
	
    def __init__(self):
		# create the 'bestprice' object
        
        print('Object of class bestprice has been created.')

        
    def scrape_bestprice_page(self, category, brand_info, ith):
		# scrapes all the products of a page and saves the data in a .csv file
		
		# define global variables
        global cnt_pages
        global proxy_pool
        global n_site
        
        category_ = category['Category']
        subcategory = category['SubCategory']
        basic_url = category['url']
        brand_name = brand_info['brand_name']
        brand_url = brand_info['brand_url']
        next_page = brand_url.format(ith)
        
		# define the path of the csv file in which the scraped data will be saved
        csvFileName = '/home/desktop/dissertation/results/' + category['Category'] + '-' + category['SubCategory']+'.csv'
        
        try:
			# increase the counter each time a page is scraped
            cnt_pages += 1

			# change the site from which we scrape proxies every 5 pages
            if cnt_pages%5==True:
                if n_site%2==0:
                    site = 1
                else:
                    site = 2
					
				# scrape proxies from the corresponding site
                proxy_pool = update_proxy_pool(site)
                print('proxy_pool is updated.')
                n_site += 1

            # try to request the page with one of the available proxies
			# try up to 20 times
            for i in range(20):
                try:
					# get a proxy from the pool and try to request the page
                    proxy = next(proxy_pool)
					
					# perform the page request and wait up to 10 seconds
                    page = requests.get(next_page, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=10)
					
                    # convert the page to a BeautifulSoup object
                    soup = BeautifulSoup(page.content, 'html.parser')
					
					# find the html tags with the product details
                    products_grid = soup.find('div', class_='grid products products--row')
                    product_divs1 = products_grid.find_all('div', class_="product__wrapper g-1 g-xsm-2 g-lg-3 g-xl-4 g-xxl-4 product__wrapper--even")
                    product_divs2 = products_grid.find_all('div', class_="product__wrapper g-1 g-xsm-2 g-lg-3 g-xl-4 g-xxl-4 product__wrapper--odd")
                    product_divs = product_divs1 + product_divs2
                    
                    break
                except Exception as e:
					# move to the next available proxy if an error occurs
                    pass


            # iterate through products of this page in order to extract their details
            for product_div in product_divs[0:]:                
                try:
					# find the html tags of the specific product
                    product_info = product_div.find('div', class_="product__main")
                    product_title_div = product_info.find('h2', class_='product__title')

					# extract the url of the product page
                    try:
                        product_url = product_title_div.find("a")['href']
                        product_page = 'https://www.bestprice.gr' + product_url
                    except:
                        product_page = None
					# extract the product title
                    try:
                        product_title = product_title_div.find("a").text
                    except:
                        product_title = None
					# extract the product description
                    try:
                        description = product_info.find('div', class_='product__description').text
                    except:
                        description = None
					# exctract the product price
                    try:
                        price = product_info.find('div', class_='product__cost-price').text
                    except:
                        price = None

					# create a dictionary to store the scraped product details
                    row = OrderedDict()
                    row['Category']= category_
                    row['SubCategory']= subcategory
                    row['url']= product_page
                    row['N']= category['N']
                    row['Title']= product_title
                    row['Price']= price
                    row['Description']= description
                    row['Page'] = ith
                    row['brand_name'] = brand_name
                    row['brand_url'] = brand_url

					# write the dictionary to the csv file
                    appendDictToCsv(filename=csvFileName, data=row)

                except Exception as e3:
					# continue to the next product if an error occurs
                    print('Error in a product: ', e3, ' - ', product_page)
                
        except Exception as e4:
			# continue to the next page if an error occurs
            print('Error #4: ', e4)
             
        
    def scrape_bestprice(self, category):
		# scrapes the product brands of the category and calls the function to scrape each product page
	
		# define a global variable
        global proxy_pool
        
		# the url of the page that will be scraped
        url = category['url']
		# the number of products that will be scraped
        n = category['N']
        
        # first scrape the available brands from the main page
        # try to request the page with one of the available proxies
		# try up to 30 times
        for i in range(30):
            try:
				# get a proxy from the pool and try to request the page
                proxy = next(proxy_pool)
				# perform the page request and wait up to 10 seconds
                page = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=10)
                # convert the page to a BeautifulSoup object
                soup = BeautifulSoup(page.content, 'html.parser')
				# find the html tags with the product brands
                filters_div = soup.find('div', id='filters')
                brand_filter_div = filters_div.find('div', class_='filter-brand default-list')
                brand_lis = brand_filter_div.find_all('li')
                break
            except Exception as e:
				# move to the next available proxy if an error occurs
                pass

		# create a list to store the information about each brand
        brand_info_list = []
		# extarct the details of each brand from the corresponding html tag
        for brand_li in brand_lis:
			# extract the url of page that refers to the brand
            brand_a = brand_li.find('a')
            brand_url = brand_a['href']
            brand_url = 'https://www.bestprice.gr' + brand_url + '&pg={}'
			# extract the name of the brand
            brand_name = brand_a.text
            brand_cnt = brand_a['data-c']
			
            # create a dictionary with the details of the brand
            brand_info = {'brand_name':brand_name, 'brand_url':brand_url, 'brand_cnt':brand_cnt}
			# append the above dictionary to the list
            brand_info_list.append(brand_info)
        
		# convert the list of dictionaries to a pandas dataframe
        df_tmp = pd.DataFrame(brand_info_list)
		# convert the datatype of  'brand_cnt' column to integer
        df_tmp['brand_cnt'] = df_tmp.brand_cnt.astype(int)

		# set counters
        total_N = 0
        i_brand = 0
		
		# for each page of each brand call the 'scrape_bestprice_page' to scrape it
        for brand_info in brand_info_list[0:]:
            i_brand += 1
            print('- Scraping category:', category['Category'], ',subcategory:', category['SubCategory'], ',brand:', brand_info['brand_name'], ' - ', i_brand, 'of', len(brand_info_list))
            
            brand_cnt = int(brand_info['brand_cnt'])
            total_N += brand_cnt
            
			# fix the pagination according to the site
            pages = int(brand_cnt/25)+2
			# scrape each page
            for i in range(1,pages):
                next_page = brand_info['brand_url'].format(i)
                print('-- Scraping page: ', next_page)
                self.scrape_bestprice_page(category, brand_info, i)
				
            # stop the process if the defined number of products have already been scraped     
            if total_N>n:
                break
                