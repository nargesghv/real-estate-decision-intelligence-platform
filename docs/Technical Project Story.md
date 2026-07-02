## Technical Project Story

I built a Real Estate Decision Intelligence Platform to support investment and portfolio planning. The project started by working with investment and strategy teams to understand decisions such as which regions to invest in, how demand may change, how interest rates affect affordability, and how new construction affects supply risk.

I translated those business questions into measurable KPIs including housing demand growth, regional price growth, employment growth, inventory, construction activity, affordability index, rent yield, months of supply, and forecast uncertainty.

On the data side, I designed a lakehouse-style pipeline with raw, clean, and curated layers. Raw data came from spreadsheets, APIs, public records, real estate portals, and economic indicators. The clean layer standardized schemas, units, timestamps, and region names. The curated layer contained fact and dimension tables used by forecasting models and Power BI dashboards.

For modeling, I used ARIMA as a time-series baseline, XGBoost for nonlinear feature-based forecasting, and DeepAR for probabilistic forecasts with uncertainty intervals. I used walk-forward validation instead of random split because the problem was forecasting. Evaluation metrics included RMSE, MAE, MAPE, directional accuracy, and prediction interval coverage.

The forecast outputs were written back to the curated layer and connected to Power BI. The dashboard helped users compare regions, evaluate supply-demand balance, monitor affordability risk, and review forecast scenarios.

## KPI Questions

### How did you choose KPIs?
I started from business decisions. If a metric did not help decide whether to invest, hold, or avoid a region, I removed it.

### Why not only price growth?
Price growth alone can be misleading. A region may grow fast but have weak affordability or future oversupply.

### How did you evaluate KPIs?
I checked data availability, business relevance, historical behavior, stakeholder feedback, and whether each KPI could be tracked monthly or quarterly.

### Which KPIs mattered most?
Demand growth, supply pressure, affordability, employment growth, and forecast uncertainty.

### How did you evaluate models?
Using walk-forward validation, RMSE, MAE, MAPE, directional accuracy, and prediction interval coverage.
