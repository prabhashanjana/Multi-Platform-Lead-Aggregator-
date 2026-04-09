from scrapers.craigslist import scrape_listings as cl_scrape
from scrapers.rightmove import scrape_listings as rm_scrape
from pipeline.normalise import normalise
from pipeline.deduplicate import deduplicate
from pipeline.validate import validate
from outputs.sheets import push_to_sheets
from outputs.email_digest import send_digest
from config import SEARCH_URL_CRAIGSLIST, SEARCH_URL_RIGHTMOVE, logger


def main() -> None:
    # Step 1 — Craigslist
    cl_data = []
    try:
        cl_data = cl_scrape(SEARCH_URL_CRAIGSLIST)
    except Exception as e:
        logger.error(f"Craigslist scraper failed: {e}")

    # Step 2 — Rightmove
    rm_data = []
    try:
        rm_data = rm_scrape(SEARCH_URL_RIGHTMOVE)
    except Exception as e:
        logger.error(f"Rightmove scraper failed: {e}")

    # Step 3 — Combine
    combined = cl_data + rm_data
    if not combined:
        logger.warning("No data from either platform — exiting")
        return

    # Step 4 to 8 — Pipeline
    df = normalise(combined)
    df = deduplicate(df)
    df = validate(df)
    push_to_sheets(df)
    send_digest(df)
    logger.info(f"Pipeline complete — {len(df)} records processed")

    logger.info("Pipeline complete")


if __name__ == "__main__":
    main()
