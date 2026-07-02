# Model Training and Evaluation

## Goal

Predict future average property price by region, property type, and month.

## Input

```text
data/curated/fact_market_monthly.csv
```

## Outputs

```text
data/curated/fact_market_forecast_predictions.csv
data/curated/model_evaluation_metrics.csv
```

These outputs are saved back into the curated layer so Power BI can visualize model results.

## Target

```text
avg_price
```

## Features

The training pipeline creates:

- price lag features
- sales lag features
- inventory lag features
- rolling 3-month price average
- rolling 3-month sales average
- month/year seasonality
- affordability index
- months of supply
- rent yield
- demand score
- employment growth
- interest rate
- construction permits

## Models

### Baseline

Previous month's price.

### XGBoost-style model

Uses GradientBoostingRegressor locally. In production this maps to SageMaker XGBoost.

### DeepAR-style model

Creates probabilistic forecast-like output with lower and upper bounds. In production this maps to SageMaker DeepAR.

### Weighted Ensemble

Combines:

```text
60% XGBoost-style prediction
40% DeepAR-style prediction
```

## Evaluation Metrics

- MAE
- RMSE
- MAPE
- Directional accuracy
- Prediction interval coverage

## Why time-based split?

Because this is forecasting. Random splits leak future information.

## Run

```bash
python src/models/train_forecasting_models.py
```
