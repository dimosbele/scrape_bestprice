# scrape_bestprice
Scrape bestprice.gr via proxies

This is a scraper that was created in order to gather data from 'bestprice.gr'. It is a commercial site where a customer can compare the price of products across different e-shops. A huge variety of product categories and subcategories is available. The main issue that we try to tackle are the sites anti-scraping measures. In particular, the site is blocking scrapers and crawlers that perform too many requests in short time. We overcome this issue by adding a functionality to the scraper so that it can change IP every five requests. This was accomplished by scraping two different sites that offer free proxies. In that way, the scraper was able to request and scrape thousands of pages without getting blocked as a bot.
