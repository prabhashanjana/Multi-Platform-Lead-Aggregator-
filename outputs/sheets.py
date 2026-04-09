import gspread
from config import GOOGLE_SHEETS_URL, SERVICE_ACCOUNT_PATH
from config import logger
import pandas as pd


def push_to_sheets(df: pd.DataFrame) -> None:
    try:
        gc = gspread.service_account(filename=SERVICE_ACCOUNT_PATH)
        sheet = gc.open_by_url(GOOGLE_SHEETS_URL)
        worksheet = sheet.worksheet("Leads")

        worksheet.clear()
        worksheet.append_row(
            ["title", "price", "location", "url", "posted_at", "source"])

        new_rows = df.copy()
        new_rows = new_rows.astype(object).where(new_rows.notna(), "")
        new_rows = new_rows.astype(str)
        new_rows = new_rows.where(new_rows != "nan", "")
        new_rows = new_rows.where(new_rows != "NaT", "")

        if new_rows.empty:
            logger.info("No new rows to append")
            return

        worksheet.append_rows(new_rows.values.tolist())
        logger.info(
            f"Appended {len(new_rows)} new rows, skipped {len(df) - len(new_rows)} duplicates")

    except Exception as e:
        logger.error(f"Failed to connect to Google Sheets: {e}")
        return
