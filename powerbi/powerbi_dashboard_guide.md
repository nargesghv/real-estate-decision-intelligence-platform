# Power BI Dashboard Guide

## Load These Tables
- fact_market_monthly.csv
- fact_market_forecast.csv
- dim_region.csv
- dim_property_type.csv

## Dashboard Pages
1. Executive Overview
2. Regional Comparison
3. Demand and Supply
4. Affordability and Interest Rate Risk
5. Forecast Scenario Analysis
6. Investment Recommendation Matrix
7. Model and Data Quality Monitoring

## DAX Measures

Average Price = AVERAGE(fact_market_monthly[avg_price])

Total Sales Volume = SUM(fact_market_monthly[sales_volume])

Total Inventory = SUM(fact_market_monthly[inventory])

Months of Supply = DIVIDE([Total Inventory], [Total Sales Volume])

Rent Yield = AVERAGE(fact_market_monthly[rent_yield])

Average Affordability Index = AVERAGE(fact_market_monthly[affordability_index])

Average Demand Score = AVERAGE(fact_market_monthly[demand_score])

Price Growth MoM = AVERAGE(fact_market_monthly[price_growth_mom])

Forecast Uncertainty = AVERAGE(fact_market_forecast[upper_bound] - fact_market_forecast[lower_bound])

Investment Score =
([Average Demand Score] * 0.30)
+ ([Price Growth MoM] * 0.20)
+ ([Rent Yield] * 0.20)
- ([Average Affordability Index] * 0.10)
- ([Forecast Uncertainty] * 0.000001)
