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

if not all([SERVICE_ACCOUNT_FILE, PROJECT_ID, DATASET_ID, TABLE_ID]):
    raise ValueError("Missing required environment variables.")

client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)

# Get today's date for filename
csv_date = pd.Timestamp.today().strftime('%Y-%m-%d')

# Query to group cost by project, service, and usage date
query = f"""
    SELECT 
        DATE(usage_start_time) AS usage_date,
        project.id AS project_id,
        service.description AS service_name,
        SUM(cost) AS total_cost,
        currency
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    WHERE DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
    GROUP BY usage_date, project_id, service_name, currency
    ORDER BY usage_date DESC, total_cost DESC
"""

# Execute query
query_job = client.query(query)
df = query_job.result().to_dataframe()

# Save to CSV with the current date
csv_filename = f"gcp_cost_by_project_service.csv"
df.to_csv(csv_filename, index=False)

print(f"Cost data by project & service saved to {csv_filename}")
