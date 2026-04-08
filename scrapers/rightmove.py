from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
from config import logger


def scrape_listings(search_url: str) -> list[dict]:

    with sync_playwright() as p:
        data = []
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        Stealth().apply_stealth_sync(page)
        page.goto(search_url, wait_until="domcontentloaded", timeout=60000)

        try:
            page.locator(
                "button[id='onetrust-accept-btn-handler']").click(timeout=5000)
            logger.info("Accepted cookies")
            page.wait_for_timeout(2000)
        except Exception:
            pass  # no cookie banner, continue
        page.wait_for_timeout(3000)

        cards = page.locator("[data-testid^='propertyCard-vrt']").all()
        total = len(cards)
        logger.info(f"Found {total} listings on Rightmove")

        for i, card in enumerate(cards):
            try:

                try:
                    href = card.locator(
                        "a[data-testid='property-details-lozenge']").get_attribute("href", timeout=2000)
                    url = f"https://www.rightmove.co.uk{href}" if href else None
                except Exception:
                    url = None

                try:
                    title = card.locator("address").inner_text(timeout=2000)
                except Exception:
                    title = None

                try:
                    location = card.locator(
                        "[data-testid='property-address']").inner_text(timeout=2000)
                except Exception:
                    location = title  # fallback to address

                try:
                    price = card.locator(
                        ".PropertyPrice_price__VL65t").inner_text(timeout=2000)

                except Exception:
                    price = None

                try:
                    posted_at = card.locator(
                        ".MarketedBy_addedOrReduced__Vtc9o").inner_text(timeout=2000)
                except Exception:
                    posted_at = None

                item = {
                    "title": title,
                    "price": price,
                    "location": location,
                    "url": url,
                    "posted_at": posted_at,
                    "source": "rightmove"
                }
                data.append(item)
                logger.info(f"Card {i+1}: {title} | {price} | {posted_at}")

            except Exception as e:
                logger.warning(f"Card {i+1} failed: {e}")
                page.screenshot(path=f"screenshots/rightmove_error_{i+1}.png")
                continue

        browser.close()
        return data
