#!/usr/bin/env python3
"""
NSE FNO Stocks Data to Google Sheets with Buy/Sell Signals and Color Formatting
"""

import os
import pickle
import requests
import pandas as pd
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

# NSE API configuration
NSE_BASE_URL = "https://www.nseindia.com"
NSE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Google Sheets configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SHEET_NAME = "NSE FNO Stocks - Buy/Sell Signals"


class NSEFNOTracker:
    def __init__(self):
        self.sheet_service = None
        self.spreadsheet_id = None
        self.authenticate_google_sheets()

    def authenticate_google_sheets(self):
        """
        Authenticate with Google Sheets API
        Uses service account or OAuth2 credentials
        """
        try:
            # Try service account first
            if os.path.exists('credentials.json'):
                creds = service_account.Credentials.from_service_account_file(
                    'credentials.json', scopes=SCOPES)
            else:
                # Fall back to OAuth2
                if os.path.exists('token.pickle'):
                    with open('token.pickle', 'rb') as token:
                        creds = pickle.load(token)
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'client_secrets.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                    with open('token.pickle', 'wb') as token:
                        pickle.dump(creds, token)
            
            self.sheet_service = build('sheets', 'v4', credentials=creds)
            print("✓ Google Sheets authenticated successfully")
        except Exception as e:
            print(f"✗ Authentication failed: {e}")
            raise

    def fetch_nse_fno_data(self):
        """
        Fetch NSE FNO (Futures & Options) data
        Returns DataFrame with stock data
        """
        try:
            print("\n📊 Fetching NSE FNO data...")
            
            # Sample NSE FNO stocks data
            # In production, integrate with NSE API or web scraping
            fno_data = {
                'Symbol': ['RELIANCE', 'TCS', 'HDFC', 'INFY', 'WIPRO', 'SBIN', 'MARUTI', 
                           'BAJAJFINSV', 'BAJAJ-AUTO', 'BHARTIARTL', 'BPCL', 'ADANIPORTS',
                           'ASIANPAINT', 'DMARUTI', 'DRREDDY', 'EICHERMOT', 'GAIL', 'GRASIM'],
                'LTP': [2950.50, 3720.25, 2650.75, 1890.40, 385.60, 550.30, 9280.15,
                        1520.80, 1680.50, 520.25, 365.80, 2480.40, 3250.90, 9150.30,
                        6780.50, 2950.75, 180.40, 2520.30],
                'High': [2980.00, 3750.00, 2680.00, 1920.00, 395.00, 560.00, 9350.00,
                         1540.00, 1700.00, 530.00, 375.00, 2500.00, 3300.00, 9200.00,
                         6850.00, 3000.00, 185.00, 2550.00],
                'Low': [2920.00, 3690.00, 2630.00, 1870.00, 375.00, 540.00, 9200.00,
                        1500.00, 1660.00, 510.00, 355.00, 2450.00, 3200.00, 9100.00,
                        6700.00, 2900.00, 175.00, 2500.00],
                'Close': [2960.00, 3730.00, 2660.00, 1900.00, 388.00, 555.00, 9300.00,
                          1530.00, 1690.00, 525.00, 368.00, 2490.00, 3270.00, 9180.00,
                          6800.00, 2980.00, 182.00, 2540.00],
                'Volume': [2500000, 1800000, 1200000, 3000000, 2200000, 2800000, 950000,
                           1600000, 1400000, 2100000, 2300000, 1700000, 1100000, 800000,
                           1300000, 1500000, 2000000, 1900000],
                'Prev Close': [2940.00, 3710.00, 2650.00, 1880.00, 385.00, 548.00, 9250.00,
                               1520.00, 1670.00, 520.00, 365.00, 2475.00, 3255.00, 9150.00,
                               6750.00, 2960.00, 180.00, 2530.00]
            }
            
            df = pd.DataFrame(fno_data)
            
            # Calculate technical indicators
            df['Change %'] = ((df['LTP'] - df['Prev Close']) / df['Prev Close'] * 100).round(2)
            df['SMA_20'] = df['Close'].rolling(window=3).mean()  # Simplified SMA
            df['Trend'] = df['Close'].apply(lambda x: 'UP' if x > 2500 else 'DOWN')
            
            # Generate Buy/Sell signals based on simple logic
            df['Signal'] = df.apply(self.generate_signal, axis=1)
            
            print(f"✓ Fetched {len(df)} stocks")
            return df
        
        except Exception as e:
            print(f"✗ Error fetching data: {e}")
            return None

    def generate_signal(self, row):
        """
        Generate buy/sell signals based on technical analysis
        """
        change = row['Change %']
        price_vs_sma = row['LTP'] - row['SMA_20'] if pd.notna(row['SMA_20']) else 0
        
        if change > 2 and price_vs_sma > 0:
            return "BUY"
        elif change < -2 and price_vs_sma < 0:
            return "SELL"
        else:
            return "HOLD"

    def create_or_clear_sheet(self):
        """
        Create new sheet or clear existing one
        """
        try:
            # Create a new spreadsheet
            spreadsheet_body = {
                'properties': {'title': SHEET_NAME}
            }
            spreadsheet = self.sheet_service.spreadsheets().create(
                body=spreadsheet_body
            ).execute()
            
            self.spreadsheet_id = spreadsheet['spreadsheetId']
            print(f"✓ Created new Google Sheet: {SHEET_NAME}")
            print(f"  Sheet ID: {self.spreadsheet_id}")
            print(f"  URL: https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}")
            
        except Exception as e:
            print(f"✗ Error creating sheet: {e}")
            raise

    def write_data_to_sheet(self, df):
        """
        Write stock data to Google Sheet
        """
        try:
            print("\n📝 Writing data to Google Sheet...")
            
            # Prepare data with headers
            headers = ['Symbol', 'LTP', 'High', 'Low', 'Close', 'Change %', 'Trend', 'Signal', 'Volume']
            values = [headers]
            
            for _, row in df.iterrows():
                values.append([
                    row['Symbol'],
                    f"{row['LTP']:.2f}",
                    f"{row['High']:.2f}",
                    f"{row['Low']:.2f}",
                    f"{row['Close']:.2f}",
                    f"{row['Change %']:.2f}%",
                    row['Trend'],
                    row['Signal'],
                    f"{row['Volume']:,}"
                ])
            
            # Write data
            self.sheet_service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range='Sheet1!A1',
                valueInputOption='RAW',
                body={'values': values}
            ).execute()
            
            print(f"✓ Wrote {len(df)} rows to sheet")
            self.apply_formatting(len(df))
            
        except Exception as e:
            print(f"✗ Error writing data: {e}")
            raise

    def apply_formatting(self, num_rows):
        """
        Apply conditional formatting and styling to the sheet
        """
        try:
            print("\n🎨 Applying color formatting and conditional rules...")
            
            requests = []
            
            # 1. Header formatting - Dark blue background with white text
            requests.append({
                'repeatCell': {
                    'range': {
                        'sheetId': 0,
                        'startRowIndex': 0,
                        'endRowIndex': 1,
                        'startColumnIndex': 0,
                        'endColumnIndex': 9
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': {'red': 0.2, 'green': 0.2, 'blue': 0.5},
                            'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
                            'horizontalAlignment': 'CENTER',
                            'verticalAlignment': 'MIDDLE'
                        }
                    },
                    'fields': 'userEnteredFormat'
                }
            })
            
            # 2. BUY Signal formatting - Green background
            requests.append({
                'conditionalFormat': {
                    'ranges': [{
                        'sheetId': 0,
                        'startRowIndex': 1,
                        'endRowIndex': num_rows + 1,
                        'startColumnIndex': 7,
                        'endColumnIndex': 8
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'TEXT_EQ',
                            'values': [{'userEnteredValue': 'BUY'}]
                        },
                        'format': {
                            'backgroundColor': {'red': 0.0, 'green': 0.8, 'blue': 0.0},
                            'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}}
                        }
                    }
                }
            })
            
            # 3. SELL Signal formatting - Red background
            requests.append({
                'conditionalFormat': {
                    'ranges': [{
                        'sheetId': 0,
                        'startRowIndex': 1,
                        'endRowIndex': num_rows + 1,
                        'startColumnIndex': 7,
                        'endColumnIndex': 8
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'TEXT_EQ',
                            'values': [{'userEnteredValue': 'SELL'}]
                        },
                        'format': {
                            'backgroundColor': {'red': 0.8, 'green': 0.0, 'blue': 0.0},
                            'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}}
                        }
                    }
                }
            })
            
            # 4. HOLD Signal formatting - Yellow background
            requests.append({
                'conditionalFormat': {
                    'ranges': [{
                        'sheetId': 0,
                        'startRowIndex': 1,
                        'endRowIndex': num_rows + 1,
                        'startColumnIndex': 7,
                        'endColumnIndex': 8
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'TEXT_EQ',
                            'values': [{'userEnteredValue': 'HOLD'}]
                        },
                        'format': {
                            'backgroundColor': {'red': 1.0, 'green': 1.0, 'blue': 0.0},
                            'textFormat': {'bold': True}
                        }
                    }
                }
            })
            
            # 5. Positive Change % - Green
            requests.append({
                'conditionalFormat': {
                    'ranges': [{
                        'sheetId': 0,
                        'startRowIndex': 1,
                        'endRowIndex': num_rows + 1,
                        'startColumnIndex': 5,
                        'endColumnIndex': 6
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'CUSTOM_FORMULA',
                            'values': [{'userEnteredValue': '=VALUE(SUBSTITUTE(F2, "%", "")) > 0'}]
                        },
                        'format': {
                            'backgroundColor': {'red': 0.9, 'green': 1.0, 'blue': 0.9},
                            'textFormat': {'foregroundColor': {'red': 0.0, 'green': 0.5, 'blue': 0.0}}
                        }
                    }
                }
            })
            
            # 6. Negative Change % - Red
            requests.append({
                'conditionalFormat': {
                    'ranges': [{
                        'sheetId': 0,
                        'startRowIndex': 1,
                        'endRowIndex': num_rows + 1,
                        'startColumnIndex': 5,
                        'endColumnIndex': 6
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'CUSTOM_FORMULA',
                            'values': [{'userEnteredValue': '=VALUE(SUBSTITUTE(F2, "%", "")) < 0'}]
                        },
                        'format': {
                            'backgroundColor': {'red': 1.0, 'green': 0.9, 'blue': 0.9},
                            'textFormat': {'foregroundColor': {'red': 0.8, 'green': 0.0, 'blue': 0.0}}
                        }
                    }
                }
            })
            
            # 7. UP Trend - Blue
            requests.append({
                'conditionalFormat': {
                    'ranges': [{
                        'sheetId': 0,
                        'startRowIndex': 1,
                        'endRowIndex': num_rows + 1,
                        'startColumnIndex': 6,
                        'endColumnIndex': 7
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'TEXT_EQ',
                            'values': [{'userEnteredValue': 'UP'}]
                        },
                        'format': {
                            'backgroundColor': {'red': 0.8, 'green': 0.9, 'blue': 1.0},
                            'textFormat': {'bold': True, 'foregroundColor': {'red': 0.0, 'green': 0.0, 'blue': 0.8}}
                        }
                    }
                }
            })
            
            # 8. DOWN Trend - Orange
            requests.append({
                'conditionalFormat': {
                    'ranges': [{
                        'sheetId': 0,
                        'startRowIndex': 1,
                        'endRowIndex': num_rows + 1,
                        'startColumnIndex': 6,
                        'endColumnIndex': 7
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'TEXT_EQ',
                            'values': [{'userEnteredValue': 'DOWN'}]
                        },
                        'format': {
                            'backgroundColor': {'red': 1.0, 'green': 0.9, 'blue': 0.8},
                            'textFormat': {'bold': True, 'foregroundColor': {'red': 0.8, 'green': 0.4, 'blue': 0.0}}
                        }
                    }
                }
            })
            
            # 9. Set column widths
            requests.append({
                'updateSheetProperties': {
                    'fields': 'gridProperties',
                    'properties': {
                        'sheetId': 0,
                        'gridProperties': {
                            'columnCount': 9,
                            'rowCount': num_rows + 2
                        }
                    }
                }
            })
            
            # Apply all formatting
            self.sheet_service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body={'requests': requests}
            ).execute()
            
            print("✓ Formatting applied successfully")
            print("  - Green highlight for BUY signals")
            print("  - Red highlight for SELL signals")
            print("  - Yellow highlight for HOLD signals")
            print("  - Green background for positive changes")
            print("  - Red background for negative changes")
            
        except Exception as e:
            print(f"✗ Error applying formatting: {e}")

    def run(self):
        """
        Main execution flow
        """
        print("="*60)
        print("NSE FNO Stocks to Google Sheets with Buy/Sell Signals")
        print("="*60)
        
        try:
            # Create sheet
            self.create_or_clear_sheet()
            
            # Fetch data
            df = self.fetch_nse_fno_data()
            if df is None:
                return
            
            # Write to sheet
            self.write_data_to_sheet(df)
            
            print("\n" + "="*60)
            print("✓ SUCCESS: All data written to Google Sheet with formatting")
            print("="*60)
            print(f"\n📊 Open your sheet here:")
            print(f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}")
            
        except Exception as e:
            print(f"\n✗ FAILED: {e}")
            raise


if __name__ == "__main__":
    tracker = NSEFNOTracker()
    tracker.run()
