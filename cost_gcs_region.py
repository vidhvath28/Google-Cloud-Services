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

client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)

# Query to group cost by region
query = f"""
    SELECT 
        location.region AS region,
        SUM(cost) AS total_cost,
        currency
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    WHERE DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
    GROUP BY region, currency
    ORDER BY total_cost DESC
"""

# Execute query
query_job = client.query(query)
df = query_job.result().to_dataframe()

# Save to CSV
df.to_csv("gcp_cost_by_region.csv", index=False)
print("Cost data by region saved to gcp_cost_by_region.csv")
