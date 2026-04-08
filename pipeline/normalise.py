import pandas as pd
import pandera as pa
from config import logger


def normalise(raw_records: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(raw_records)

    # claen data
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda col: col.str.strip())

    df["title"] = df["title"].str.title()    # Amal Perera
    df['price'] = df['price'].str.replace(r'[^\d.]', '', regex=True)
    df["location"] = df["location"].str.lower()
    df["posted_at"] = df["posted_at"].str.extract(
        r'(\d{2}/\d{2}/\d{4}|\w+ \w+ \d{2} \d{4})')
    df["posted_at"] = pd.to_datetime(df["posted_at"], errors="coerce")

    logger.info(f"Normalised {len(df)} records")

    for source, count in df["source"].value_counts().items():
        logger.info(f"  {source}: {count} records")

    return df
