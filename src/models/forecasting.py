import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

def evaluate_forecast(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = mean_squared_error(y_true, y_pred, squared=False)
    mape = np.mean(np.abs((np.array(y_true) - np.array(y_pred)) / np.array(y_true))) * 100
    return {"MAE": mae, "RMSE": rmse, "MAPE": mape}

def weighted_ensemble(xgb_pred, deepar_pred, xgb_weight=0.55):
    return (xgb_weight * np.array(xgb_pred)) + ((1 - xgb_weight) * np.array(deepar_pred))
