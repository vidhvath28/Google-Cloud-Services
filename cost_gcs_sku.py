import os
import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up BigQuery Client
SERVICE_ACCOUNT_FILE = os.getenv("GCP_SERVICE_ACCOUNT_KEY")
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = os.getenv("GCP_BILLING_DATASET")
TABLE_ID = os.getenv("GCP_BILLING_TABLE")

if not SERVICE_ACCOUNT_FILE or not PROJECT_ID or not DATASET_ID or not TABLE_ID:
    raise ValueError("Missing required environment variables.")

client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)

# Query to group cost by SKU and date
query = f"""
    SELECT 
        DATE(usage_start_time) AS usage_date,
        sku.description AS sku_name,
        SUM(cost) AS total_cost,
        currency
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    WHERE DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
    GROUP BY usage_date, sku_name, currency
    ORDER BY usage_date DESC, total_cost DESC
"""

# Execute query
query_job = client.query(query)
df = query_job.result().to_dataframe()

# Ensure file is saved as .csv
csv_filename = "gcp_cost_by_sku.csv"
if not csv_filename.endswith(".csv"):
    csv_filename += ".csv"

df.to_csv(csv_filename, index=False)

print(f"Cost data by SKU and date saved to {csv_filename}")
