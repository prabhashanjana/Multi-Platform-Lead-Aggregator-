import pandas as pd
import pandera.pandas as pa
from pandera import Column, DataFrameSchema, Check
from config import logger


def validate(df: pd.DataFrame) -> pd.DataFrame:
    schema = DataFrameSchema({
        "title": Column(str, nullable=True),
        "price": Column(str, nullable=True),
        "location": Column(str, nullable=True),
        "url": Column(str, nullable=True),
        "posted_at": Column(pa.DateTime, nullable=True),
        "source": Column(str, nullable=False, checks=Check.isin(["craigslist", "rightmove"]))
    })

    try:
        validated_df = schema.validate(df)
        logger.info(f"Validated {len(validated_df)} records successfully")
        return validated_df
    except pa.errors.SchemaError as e:
        logger.warning(f"Validation warning: {e.failure_cases}")
        return df
