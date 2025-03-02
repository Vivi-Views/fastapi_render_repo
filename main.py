from fastapi import FastAPI, HTTPException
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = FastAPI()

# Load Google Sheets Credentials from Environment Variable
google_creds = json.loads(os.getenv("GOOGLE_SHEETS_CREDENTIALS"))

# Authenticate with Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(google_creds, scope)
client = gspread.authorize(creds)

# Open your Google Sheet (Replace "Hindu Services Data" with your actual sheet name)
sheet = client.open("Hindu Services Data").sheet1

@app.get("/")
def read_root():
    return {"message": "FastAPI on Render is working!"}

@app.post("/submit")
async def submit_data(data: dict):
    try:
        row_data = [
            data.get("poojalu"), data.get("nomulu"), data.get("vrataalu"),
            data.get("daanaalu"), data.get("japaalu"), data.get("karmalu"),
            data.get("krathuvulu"), data.get("apara_karmalu")
        ]
        sheet.append_row(row_data)
        return {"message": "Data added successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

