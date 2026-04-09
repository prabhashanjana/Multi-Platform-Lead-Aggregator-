from scrapers.craigslist import scrape_listings as cl_scrape
from scrapers.rightmove import scrape_listings as rm_scrape
from pipeline.normalise import normalise
from pipeline.deduplicate import deduplicate
from pipeline.validate import validate
from config import SEARCH_URL_CRAIGSLIST, SEARCH_URL_RIGHTMOVE
from outputs.sheets import push_to_sheets
import pandas as pd
from outputs.email_digest import send_digest

cl_data = cl_scrape(SEARCH_URL_CRAIGSLIST)
rm_data = rm_scrape(SEARCH_URL_RIGHTMOVE)

combined = cl_data + rm_data
df = normalise(combined)
df = deduplicate(df)
df = validate(df)

print(df.head())
print(f"Final record count: {len(df)}")
df.to_csv("test_data.csv", index=False)
push_to_sheets(df)
send_digest(df)
