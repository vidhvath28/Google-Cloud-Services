import streamlit as st
import os
import datetime
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Load Google Drive API credentials
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE") or r"C:\Yellow.ai\Google-Cloud-Services\grafana-cost-management-4470e527209e.json"
ROOT_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID") or "1USaI7qHuUfj2wDUD13eg-xFqMC7cD17j"

# Validate environment variables
if not os.path.exists(SERVICE_ACCOUNT_FILE):
    st.error(f"Error: Service account file not found at {SERVICE_ACCOUNT_FILE}")
    st.stop()

if not ROOT_FOLDER_ID:
    st.error("Error: GOOGLE_DRIVE_FOLDER_ID is not set.")
    st.stop()

# Authenticate with Google Drive API
def authenticate_google_drive():
    try:
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
        service = build("drive", "v3", credentials=creds)
        return service
    except Exception as e:
        st.error(f"Google Drive authentication failed: {e}")
        st.stop()

# Get today's folder structure
today = datetime.datetime.today()
folder_structure = f"GCS/{today.year}/{today.month}/{today.day}"

# Function to get folder ID by name (inside a parent folder)
def get_folder_id(service, parent_id, folder_name):
    query = f"'{parent_id}' in parents and name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields="files(id)").execute()
    folders = results.get("files", [])
    return folders[0]["id"] if folders else None

# Function to list all files and folders inside a folder
def list_files_in_folder(service, folder_id):
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    return results.get("files", [])

# Streamlit UI
st.title(f"📂 Google Drive Viewer - {folder_structure}")

# Authenticate
service = authenticate_google_drive()

# Navigate through the folder structure dynamically
gcs_folder_id = get_folder_id(service, ROOT_FOLDER_ID, "GCS")
if not gcs_folder_id:
    st.error("GCS folder not found!")
    st.stop()

year_folder_id = get_folder_id(service, gcs_folder_id, str(today.year))
if not year_folder_id:
    st.warning(f"No folder found for year {today.year}.")
    st.stop()

month_folder_id = get_folder_id(service, year_folder_id, str(today.month))
if not month_folder_id:
    st.warning(f"No folder found for month {today.month}.")
    st.stop()

day_folder_id = get_folder_id(service, month_folder_id, str(today.day))
if not day_folder_id:
    st.warning(f"No folder found for day {today.day}. No files available.")
    st.stop()

# List all files in today's folder
files = list_files_in_folder(service, day_folder_id)

if files:
    st.write("### 📄 Files in today's folder:")
    for file in files:
        if file["mimeType"] == "application/vnd.google-apps.folder":
            st.markdown(f"📂 **{file['name']}** (Folder)")  # Show folders without expanders
        else:
            st.markdown(f"📄 **{file['name']}** _(Type: {file['mimeType_
