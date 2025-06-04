import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os

# Tambahkan path ke folder utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.load import store_to_csv, store_to_gsheet

class TestLoadFunctions(unittest.TestCase):

    @patch('utils.load.pd.DataFrame.to_csv')
    def test_store_to_csv(self, mock_to_csv):
        data = pd.DataFrame({'Title': ['Product 1'], 'Price': [500]})
        store_to_csv(data, "output.csv")
        mock_to_csv.assert_called_once_with("output.csv", index=False)

    @patch('utils.load.gspread.authorize')
    @patch('utils.load.Credentials')
    def test_store_to_gsheet(self, mock_credentials, mock_authorize):
        # Mock credentials dan client gspread
        mock_creds = MagicMock()
        mock_credentials.from_service_account_file.return_value = mock_creds

        mock_client = MagicMock()
        mock_authorize.return_value = mock_client

        mock_spreadsheet = MagicMock()
        mock_worksheet = MagicMock()

        mock_client.open.return_value = mock_spreadsheet
        mock_spreadsheet.get_worksheet.return_value = mock_worksheet

        data = pd.DataFrame({'Title': ['Product 1'], 'Price': [500]})

        store_to_gsheet(data, "Test Sheet", "credentials.json")

        mock_credentials.from_service_account_file.assert_called_once_with(
            "credentials.json",
            scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        )
        mock_authorize.assert_called_once_with(mock_creds)
        mock_client.open.assert_called_once_with("Test Sheet")
        mock_spreadsheet.get_worksheet.assert_called_once_with(0)
        mock_worksheet.clear.assert_called_once()
        mock_worksheet.update.assert_called_once()

if __name__ == "__main__":
    unittest.main()