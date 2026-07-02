# Project Walkthrough

from src.ingestion.market_ingestion import ingest_raw_market_data, basic_raw_validation
from src.transformation.clean_market import clean_market_data, create_kpis
from src.features.feature_engineering import create_forecasting_features

raw = ingest_raw_market_data("../data/raw/market/monthly_real_estate_market.csv")
print(basic_raw_validation(raw))

clean = clean_market_data(raw)
curated = create_kpis(clean)
features = create_forecasting_features(curated)

print(features.head())
