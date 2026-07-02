
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CURATED_INPUT_PATH = PROJECT_ROOT / "data" / "curated" / "fact_market_monthly.csv"
PREDICTION_OUTPUT_PATH = PROJECT_ROOT / "data" / "curated" / "fact_market_forecast_predictions.csv"
METRICS_OUTPUT_PATH = PROJECT_ROOT / "data" / "curated" / "model_evaluation_metrics.csv"


@dataclass
class ModelConfig:
    target_column: str = "avg_price"
    date_column: str = "month"
    train_end_date: str = "2025-06-01"
    test_start_date: str = "2025-07-01"
    model_version: str = "real_estate_forecast_ensemble_v1"
    xgb_weight: float = 0.60
    deepar_weight: float = 0.40


def load_curated_market_data(path: Path = CURATED_INPUT_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["month"] = pd.to_datetime(df["month"])
    return df


def create_forecasting_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values(["region", "property_type", "month"])
    group_cols = ["region", "property_type"]

    for lag in [1, 3, 6, 12]:
        df[f"price_lag_{lag}"] = df.groupby(group_cols)["avg_price"].shift(lag)
        df[f"sales_lag_{lag}"] = df.groupby(group_cols)["sales_volume"].shift(lag)
        df[f"inventory_lag_{lag}"] = df.groupby(group_cols)["inventory"].shift(lag)

    df["price_rolling_3m"] = (
        df.groupby(group_cols)["avg_price"]
        .rolling(window=3)
        .mean()
        .reset_index(level=group_cols, drop=True)
    )

    df["sales_rolling_3m"] = (
        df.groupby(group_cols)["sales_volume"]
        .rolling(window=3)
        .mean()
        .reset_index(level=group_cols, drop=True)
    )

    df["month_num"] = df["month"].dt.month
    df["year"] = df["month"].dt.year
    df["region_code"] = df["region"].astype("category").cat.codes
    df["property_type_code"] = df["property_type"].astype("category").cat.codes

    return df.dropna().reset_index(drop=True)


def get_feature_columns() -> List[str]:
    return [
        "region_code", "property_type_code", "sales_volume", "inventory",
        "construction_permits", "employment_growth", "interest_rate",
        "median_income", "affordability_index", "months_of_supply",
        "rent_yield", "price_growth_mom", "demand_score",
        "price_lag_1", "price_lag_3", "price_lag_6", "price_lag_12",
        "sales_lag_1", "sales_lag_3", "sales_lag_6", "sales_lag_12",
        "inventory_lag_1", "inventory_lag_3", "inventory_lag_6", "inventory_lag_12",
        "price_rolling_3m", "sales_rolling_3m", "month_num", "year",
    ]


def time_based_split(df: pd.DataFrame, config: ModelConfig) -> Tuple[pd.DataFrame, pd.DataFrame]:
    train = df[df[config.date_column] <= pd.to_datetime(config.train_end_date)].copy()
    test = df[df[config.date_column] >= pd.to_datetime(config.test_start_date)].copy()
    return train, test


def train_gradient_boosting_model(train_df: pd.DataFrame, feature_cols: List[str], target_col: str):
    model = GradientBoostingRegressor(
        n_estimators=250,
        learning_rate=0.05,
        max_depth=3,
        random_state=42,
    )
    model.fit(train_df[feature_cols], train_df[target_col])
    return model


def create_deepar_style_forecast(test_df: pd.DataFrame) -> pd.DataFrame:
    """Local approximation of SageMaker DeepAR probabilistic output.

    Real DeepAR would learn probability distributions across many related time series.
    Here we create point predictions and uncertainty bands for portfolio demonstration.
    """
    df = test_df.copy()
    trend_component = df["price_rolling_3m"]
    recent_growth = df["price_growth_mom"].clip(lower=-0.05, upper=0.05)
    df["deepar_prediction"] = trend_component * (1 + recent_growth)

    uncertainty_factor = (
        0.04
        + df["price_growth_mom"].abs().fillna(0)
        + (df["affordability_index"].rank(pct=True) * 0.03)
    )

    df["deepar_lower_bound"] = df["deepar_prediction"] * (1 - uncertainty_factor)
    df["deepar_upper_bound"] = df["deepar_prediction"] * (1 + uncertainty_factor)
    return df


def rmse_score(y_true, y_pred) -> float:
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def evaluate_predictions(actual, prediction, model_name: str) -> Dict[str, float | str]:
    actual_np = np.array(actual)
    pred_np = np.array(prediction)
    mae = float(mean_absolute_error(actual_np, pred_np))
    rmse = rmse_score(actual_np, pred_np)
    mape = float(np.mean(np.abs((actual_np - pred_np) / actual_np)) * 100)

    actual_direction = np.sign(np.diff(actual_np))
    pred_direction = np.sign(np.diff(pred_np))
    directional_accuracy = (
        float(np.mean(actual_direction == pred_direction))
        if len(actual_direction) > 0
        else None
    )

    return {
        "model_name": model_name,
        "MAE": round(mae, 4),
        "RMSE": round(rmse, 4),
        "MAPE": round(mape, 4),
        "directional_accuracy": round(directional_accuracy, 4) if directional_accuracy is not None else None,
    }


def evaluate_prediction_intervals(df: pd.DataFrame) -> Dict[str, float | str]:
    coverage = (
        (df["avg_price"] >= df["ensemble_lower_bound"])
        & (df["avg_price"] <= df["ensemble_upper_bound"])
    ).mean()
    avg_interval_width = (
        df["ensemble_upper_bound"] - df["ensemble_lower_bound"]
    ).mean()
    return {
        "model_name": "ensemble_prediction_interval",
        "prediction_interval_coverage": round(float(coverage), 4),
        "average_interval_width": round(float(avg_interval_width), 4),
    }


def train_evaluate_and_save_predictions(config: ModelConfig = ModelConfig()) -> None:
    df = load_curated_market_data()
    feature_df = create_forecasting_features(df)
    feature_cols = get_feature_columns()
    train_df, test_df = time_based_split(feature_df, config)

    if train_df.empty or test_df.empty:
        raise ValueError("Train or test split is empty. Check date ranges and data.")

    test_df["baseline_prediction"] = test_df["price_lag_1"]

    xgb_model = train_gradient_boosting_model(train_df, feature_cols, config.target_column)
    test_df["xgb_prediction"] = xgb_model.predict(test_df[feature_cols])

    deepar_df = create_deepar_style_forecast(test_df)
    test_df["deepar_prediction"] = deepar_df["deepar_prediction"]
    test_df["deepar_lower_bound"] = deepar_df["deepar_lower_bound"]
    test_df["deepar_upper_bound"] = deepar_df["deepar_upper_bound"]

    test_df["ensemble_prediction"] = (
        config.xgb_weight * test_df["xgb_prediction"]
        + config.deepar_weight * test_df["deepar_prediction"]
    )
    test_df["ensemble_lower_bound"] = (
        config.xgb_weight * test_df["xgb_prediction"]
        + config.deepar_weight * test_df["deepar_lower_bound"]
    )
    test_df["ensemble_upper_bound"] = (
        config.xgb_weight * test_df["xgb_prediction"]
        + config.deepar_weight * test_df["deepar_upper_bound"]
    )

    test_df["model_version"] = config.model_version
    test_df["prediction_created_at"] = pd.Timestamp.utcnow()

    metrics = [
        evaluate_predictions(test_df["avg_price"], test_df["baseline_prediction"], "baseline_previous_month"),
        evaluate_predictions(test_df["avg_price"], test_df["xgb_prediction"], "xgboost_style_gradient_boosting"),
        evaluate_predictions(test_df["avg_price"], test_df["deepar_prediction"], "deepar_style_probabilistic"),
        evaluate_predictions(test_df["avg_price"], test_df["ensemble_prediction"], "weighted_ensemble"),
        evaluate_prediction_intervals(test_df),
    ]

    prediction_cols = [
        "month", "region", "property_type", "avg_price",
        "baseline_prediction", "xgb_prediction", "deepar_prediction",
        "deepar_lower_bound", "deepar_upper_bound",
        "ensemble_prediction", "ensemble_lower_bound", "ensemble_upper_bound",
        "model_version", "prediction_created_at",
    ]

    test_df[prediction_cols].to_csv(PREDICTION_OUTPUT_PATH, index=False)
    pd.DataFrame(metrics).to_csv(METRICS_OUTPUT_PATH, index=False)

    print("Training and evaluation complete.")
    print(f"Predictions saved to: {PREDICTION_OUTPUT_PATH}")
    print(f"Metrics saved to: {METRICS_OUTPUT_PATH}")
    print(pd.DataFrame(metrics))


if __name__ == "__main__":
    train_evaluate_and_save_predictions()
