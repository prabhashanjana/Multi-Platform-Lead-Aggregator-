from config import logger
import pandas as pd


def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        logger.info("No records to deduplicate")
        return df

    before = len(df)
    df = df.drop_duplicates(subset=["url"], keep="first")
    after = len(df)
    removed_url = before - after
    logger.info(
        f"Deduplicated records: {removed_url} duplicates removed based on URL, {after} unique records remain")

    before = len(df)
    df = df.drop_duplicates(
        subset=["title", "location"], keep="first")
    after = len(df)
    removed_title_location = before - after
    logger.info(
        f"Deduplicated records: {removed_title_location} duplicates removed based on title+location, {after} unique records remain")

    return df
