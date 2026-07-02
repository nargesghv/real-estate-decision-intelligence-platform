import pandas as pd

def ingest_raw_market_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def basic_raw_validation(df: pd.DataFrame) -> dict:
    return {
        "row_count": len(df),
        "column_count": len(df.columns),
        "missing_by_column": df.isna().sum().to_dict()
    }
