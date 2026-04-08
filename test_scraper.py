from scrapers.rightmove import scrape_listings as rightmove_scrape
from config import SEARCH_URL_RIGHTMOVE

results = rightmove_scrape(SEARCH_URL_RIGHTMOVE)
print(f"Total listings: {len(results)}")
if results:
    print(results[0])
