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

# Define query to fetch last 7 days' cost data
query = f"""
    SELECT 
        service.description AS service_name,
        project.id AS project_id,
        sku.description AS sku_name,
        usage_start_time,
        cost,
        currency
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    WHERE DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
    ORDER BY usage_start_time DESC
"""

# Execute the query
query_job = client.query(query)
results = query_job.result()

# Convert results to DataFrame
df = results.to_dataframe()

# Save to CSV
csv_filename = "gcp_cost_details.csv"
df.to_csv(csv_filename, index=False)
print(f"Cost data saved to {csv_filename}")
