# Multi-Platform Lead Aggregator

A Python automation tool that scrapes real estate listings from multiple platforms, deduplicates them, validates the data, and delivers a morning digest to Google Sheets and email.

## What It Does

Every morning it:
1. Scrapes listings from Craigslist and Rightmove
2. Cleans and deduplicates the data
3. Validates the schema
4. Pushes all leads to a Google Sheet
5. Emails a formatted digest with the full lead table

## Tech Stack

- **Playwright** — browser automation and scraping
- **pandas + pandera** — data processing and validation
- **gspread** — Google Sheets output
- **smtplib** — email digest delivery
- **loguru** — production logging
- **tenacity** — retry logic
- **python-dotenv** — secrets management

## Setup

**1 — Clone the repo and create a virtual environment**
```bash
git clone https://github.com/prabhashanjana/Multi-Platform-Lead-Aggregator
cd Multi-Platform-Lead-Aggregator
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

**2 — Create a `.env` file**
```
SERVICE_ACCOUNT_PATH=service_account.json
GOOGLE_SHEETS_URL=your_google_sheets_url
GMAIL_ADDRESS=your_gmail
GMAIL_APP_PASSWORD=your_app_password
RECIPIENT_EMAIL=recipient_email
SEARCH_URL_CRAIGSLIST=https://newyork.craigslist.org/search/rea
SEARCH_URL_RIGHTMOVE=https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E904
```

**3 — Add your Google service account**

Place your `service_account.json` in the project root and share your Google Sheet with the service account email as Editor.

**4 — Run the pipeline**
```bash
python main.py
```

## Project Structure
```
├── scrapers/
│   ├── craigslist.py       # Craigslist scraper
│   └── rightmove.py        # Rightmove scraper
├── pipeline/
│   ├── normalise.py        # Data cleaning
│   ├── deduplicate.py      # Deduplication
│   └── validate.py         # Schema validation
├── outputs/
│   ├── sheets.py           # Google Sheets push
│   └── email_digest.py     # Morning email digest
├── main.py                 # Orchestrator
└── requirements.txt
```

## Scheduling

Use Windows Task Scheduler to run `run.bat` daily at 7am.

## Output

- **Google Sheets** — full lead table refreshed daily
- **Email** — HTML digest with lead count and table
- **Logs** — full run log at `logs/app.log`