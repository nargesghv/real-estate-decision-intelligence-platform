import pandas as pd

def clean_market_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["month"] = pd.to_datetime(df["month"])
    df["region"] = df["region"].str.strip()
    df["property_type"] = df["property_type"].str.strip()
    return df.dropna(subset=["month", "region", "property_type", "avg_price"])

def create_kpis(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy().sort_values(["region", "property_type", "month"])
    df["affordability_index"] = df["avg_price"] / df["median_income"]
    df["months_of_supply"] = df["inventory"] / df["sales_volume"]
    df["rent_yield"] = (df["avg_rent"] * 12) / df["avg_price"]
    df["price_growth_mom"] = df.groupby(["region","property_type"])["avg_price"].pct_change().fillna(0)
    df["demand_score"] = (
        df["sales_volume"].rank(pct=True)*0.35
        + df["employment_growth"].rank(pct=True)*0.25
        + (1/df["months_of_supply"]).rank(pct=True)*0.25
        + df["price_growth_mom"].rank(pct=True)*0.15
    )
    return df
