from sqlalchemy import create_engine
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials  # gunakan ini, bukan oauth2client

def store_to_csv(data, filename="output.csv"):
    try:
        data.to_csv(filename, index=False)
        print(f"Data berhasil disimpan ke file CSV: {filename}")
    except Exception as e:
        print(f"[ERROR] CSV: {e}")

def store_to_gsheet(data, sheet_name, json_keyfile_name):
    try:
        # Setup koneksi dengan Google Sheets API menggunakan google-auth
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(json_keyfile_name, scopes=scopes)
        client = gspread.authorize(creds)

        # Akses spreadsheet dan worksheet
        spreadsheet = client.open(sheet_name)
        worksheet = spreadsheet.get_worksheet(0)  # worksheet pertama

        # Clear dan update
        worksheet.clear()
        worksheet.update([data.columns.values.tolist()] + data.values.tolist())

        print("Data berhasil ditulis ke Google Sheets!")
    except Exception as e:
        print(f"[ERROR] Google Sheets: {e}")
