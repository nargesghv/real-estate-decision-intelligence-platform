def create_forecasting_features(df):
    df = df.copy().sort_values(["region", "property_type", "month"])
    group_cols = ["region", "property_type"]
    for lag in [1, 3, 6, 12]:
        df[f"price_lag_{lag}"] = df.groupby(group_cols)["avg_price"].shift(lag)
        df[f"sales_lag_{lag}"] = df.groupby(group_cols)["sales_volume"].shift(lag)
    df["price_rolling_3m"] = df.groupby(group_cols)["avg_price"].rolling(3).mean().reset_index(level=group_cols, drop=True)
    df["sales_rolling_3m"] = df.groupby(group_cols)["sales_volume"].rolling(3).mean().reset_index(level=group_cols, drop=True)
    df["month_num"] = df["month"].dt.month
    df["year"] = df["month"].dt.year
    return df.dropna()
