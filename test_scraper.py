from scrapers.craigslist import scrape_listings
from config import SEARCH_URL_CRAIGSLIST

results = scrape_listings(SEARCH_URL_CRAIGSLIST)
print(f"Total listings: {len(results)}")


# Fix — always check first
if results:
    print(results[0])
else:
    print("No results returned")
