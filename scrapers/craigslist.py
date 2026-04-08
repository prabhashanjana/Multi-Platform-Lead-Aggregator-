from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
from config import SEARCH_URL_CRAIGSLIST, logger


def scrape_listings(search_url: str) -> list[dict]:

    with sync_playwright() as p:
        data = []
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = context.new_page()
        Stealth().apply_stealth_sync(page)
        page.goto(search_url,
                  wait_until="networkidle")

        page.wait_for_selector(".result-node")

        cards = page.locator("div[data-pid]")
        cards_list = cards.all()
        total = len(cards_list)
        logger.info(f"Found {total} leads on Craigslist")

        for i, card in enumerate(cards_list):
            try:
                try:
                    title = card.locator(".label").inner_text(timeout=2000)
                except Exception:
                    title = None
                try:
                    price = card.locator(".priceinfo").inner_text(timeout=2000)
                except Exception:
                    price = None
                try:
                    location = card.locator(
                        ".result-location").inner_text(timeout=2000)
                except Exception:
                    location = None
                try:
                    url = card.locator("a[tabindex='0']").get_attribute("href")
                except Exception:
                    url = None
                try:
                    posted_at = card.locator(
                        "div.meta span[title]").get_attribute("title")
                except Exception:
                    posted_at = None

                item = {
                    "title": title,
                    "price": price,
                    "location": location,
                    "url": url,
                    "posted_at": posted_at,
                    "source": "craigslist"
                }
                data.append(item)

                logger.info(
                    f"Card {i+1}: {title} | {price} | {location} | {posted_at}")

            except Exception as e:
                logger.warning(f"Card {i+1} failed: {e}")
                page.screenshot(path=f"screenshots/error_card_{i+1}.png")
                continue

        browser.close()
        return data
