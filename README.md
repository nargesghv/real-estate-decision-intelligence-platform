# Real Estate Decision Intelligence Platform

Portfolio project for data science, business analysis, forecasting, and BI.

## Goal
Help investment teams decide which real estate markets are attractive using KPIs, forecasting models, and Power BI dashboards.

## Architecture
Raw data -> Clean data -> Curated dimensional model -> Forecasting models -> Power BI decision dashboard.

## Technologies
Python, SQL, Spark-style data lake design, AWS S3/Glue/Redshift/SageMaker concepts, Power BI, XGBoost, DeepAR, ARIMA.

## Main KPIs
Housing demand growth, price growth, employment growth, inventory, construction permits, affordability index, months of supply, rent yield, forecast uncertainty, investment attractiveness score.

## Project Folders
- data/raw: raw market data
- data/curated: analytics-ready tables
- src: ingestion, transformation, features, modeling
- sql: KPI SQL examples
- powerbi: dashboard guide and DAX measures
- docs: architecture, KPI framework, interview guide

## Model Training

Run:

```bash
python src/models/train_forecasting_models.py
```

This creates:

```text
data/curated/fact_market_forecast_predictions.csv
data/curated/model_evaluation_metrics.csv
```

The modeling workflow includes:

- baseline previous-month model
- XGBoost-style gradient boosting model
- DeepAR-style probabilistic forecast approximation
- weighted ensemble forecast
- MAE, RMSE, MAPE, directional accuracy
- prediction interval coverage
