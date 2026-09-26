# Google Sheets API Setup Guide

## Steps to Set Up Google Sheets API Credentials

### Option 1: Using Service Account (Recommended for Automation)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Google Sheets API
4. Create a Service Account:
   - Go to "Service Accounts"
   - Click "Create Service Account"
   - Fill in details and click "Create and Continue"
   - Click "Create Key" → Select JSON → Download
5. Rename the downloaded JSON file to `credentials.json`
6. Place it in the project root directory

### Option 2: Using OAuth 2.0 (Interactive)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Google Sheets API
4. Create an OAuth 2.0 Credential:
   - Go to "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop application"
   - Click "Create"
   - Download the JSON file
5. Rename it to `client_secrets.json`
6. Place it in the project root directory

## Installation

```bash
pip install -r requirements.txt
```

## Running the Script

```bash
python nse_fno_tracker.py
```

## Output

The script will:
1. ✓ Authenticate with Google Sheets
2. ✓ Create a new Google Sheet
3. ✓ Fetch NSE FNO stocks data
4. ✓ Write data with proper formatting
5. ✓ Apply conditional formatting:
   - **Green** for BUY signals
   - **Red** for SELL signals  
   - **Yellow** for HOLD signals
   - **Green background** for positive price changes
   - **Red background** for negative price changes
   - **Blue** for UP trend
   - **Orange** for DOWN trend
6. ✓ Print the Google Sheet URL for access

## Column Meanings

- **Symbol**: Stock ticker name
- **LTP**: Last Traded Price
- **High**: Day's high price
- **Low**: Day's low price
- **Close**: Closing price
- **Change %**: Percentage change from previous close
- **Trend**: UP or DOWN trend indicator
- **Signal**: BUY, SELL, or HOLD recommendation
- **Volume**: Trading volume

## Customization

You can modify the signal generation logic in the `generate_signal()` method to use your own technical indicators.
