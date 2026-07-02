# Architecture

## Data Sources
- Real estate portals
- Public records
- Construction permits
- Employment indicators
- Interest rates
- Market surveys
- Internal spreadsheets

## Layers
Raw Layer: stores source data exactly as received.
Clean Layer: standardizes schemas, time zones, region names, units, and data types.
Curated Layer: contains fact and dimension tables for BI and modeling.

## AWS Mapping
- S3: raw, clean, curated data lake
- Glue/Lambda: ingestion and transformation
- Redshift/Athena: analytics serving
- SageMaker: model training and registry
- Power BI/QuickSight: dashboards
