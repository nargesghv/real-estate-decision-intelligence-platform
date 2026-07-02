-- KPI SQL Examples

-- Monthly price growth
SELECT
  region,
  property_type,
  month,
  avg_price,
  LAG(avg_price) OVER (
    PARTITION BY region, property_type
    ORDER BY month
  ) AS previous_price
FROM fact_market_monthly;

-- Demand and employment by region
SELECT
  region,
  month,
  SUM(sales_volume) AS total_sales_volume,
  AVG(employment_growth) AS avg_employment_growth
FROM fact_market_monthly
GROUP BY region, month;

-- Months of supply
SELECT
  region,
  property_type,
  month,
  SUM(inventory) / NULLIF(SUM(sales_volume), 0) AS months_of_supply
FROM fact_market_monthly
GROUP BY region, property_type, month;

-- Top regions by demand score
SELECT
  region,
  AVG(demand_score) AS avg_demand_score,
  AVG(rent_yield) AS avg_rent_yield,
  AVG(affordability_index) AS avg_affordability
FROM fact_market_monthly
GROUP BY region
ORDER BY avg_demand_score DESC;
