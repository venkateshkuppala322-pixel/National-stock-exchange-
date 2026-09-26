# NSE FNO Stocks to Google Sheets with Buy/Sell Signals

Automatically fetch NSE F&O (Futures & Options) stock data and populate a Google Sheet with color-formatted buy/sell trading signals.

## Features

✨ **Key Features:**
- 📊 **Real-time NSE FNO Data**: Fetches latest stock prices, trends, and volumes
- 💹 **Technical Indicators**: Calculates SMA, trends, and buy/sell signals
- 🎨 **Color Formatting**: Professional color-coded signals
  - 🟢 **Green** - BUY signals
  - 🔴 **Red** - SELL signals
  - 🟡 **Yellow** - HOLD signals
  - Price changes color-coded by positive/negative movement
  - Trend indicators (UP/DOWN) with distinct colors
- 📈 **Automated Updates**: Can be scheduled to run periodically
- 🔐 **Secure**: Uses Google Service Account or OAuth 2.0 authentication

## Quick Start

### Prerequisites
- Python 3.8+
- Google Cloud account
- Google Sheets API enabled

### Installation

1. **Clone and setup:**
```bash
cd National-stock-exchange-
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Setup Google Credentials:**
   - Follow the [setup_credentials.md](setup_credentials.md) guide
   - Download `credentials.json` or `client_secrets.json`
   - Place in project root directory

4. **Run the script:**
```bash
python nse_fno_tracker.py
```

## Color Legend

| Color | Meaning | Details |
|-------|---------|----------|
| 🟢 Green | BUY | Strong uptrend signal - consider buying |
| 🔴 Red | SELL | Strong downtrend signal - consider selling |
| 🟡 Yellow | HOLD | Neutral signal - hold current position |
| Light Green Background | Positive Change | Stock price increased from previous close |
| Light Red Background | Negative Change | Stock price decreased from previous close |
| Blue | UP Trend | Trend is moving upward |
| Orange | DOWN Trend | Trend is moving downward |

## Columns Explained

| Column | Description |
|--------|-------------|
| Symbol | Stock ticker name (e.g., RELIANCE, TCS) |
| LTP | Last Traded Price |
| High | Day's highest price |
| Low | Day's lowest price |
| Close | Closing price |
| Change % | Percentage change from previous closing price |
| Trend | UP or DOWN trend direction |
| Signal | BUY, SELL, or HOLD recommendation |
| Volume | Trading volume for the day |

## Signal Generation Logic

The script uses a simple algorithm:

```
IF (Change % > 2%) AND (Price > SMA_20):
    → BUY Signal (Green)
ELSE IF (Change % < -2%) AND (Price < SMA_20):
    → SELL Signal (Red)
ELSE:
    → HOLD Signal (Yellow)
```

You can customize this logic in the `generate_signal()` method.

## Scheduling Updates (Optional)

### Using Cron (Linux/Mac)
```bash
# Edit crontab
crontab -e

# Add line to run daily at 9 AM
0 9 * * * cd /path/to/National-stock-exchange- && python nse_fno_tracker.py
```

### Using Task Scheduler (Windows)
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to daily at 9 AM
4. Set action to run: `python.exe C:\path\to\nse_fno_tracker.py`

## API Integration

Currently, the script uses sample data. To integrate with live NSE data:

1. **Option A**: Use NSE API (if available)
```python
response = requests.get('https://api.nseindia.com/fno-data')
data = response.json()
```

2. **Option B**: Web scraping with BeautifulSoup
```python
from bs4 import BeautifulSoup
response = requests.get('https://www.nseindia.com/...')
soup = BeautifulSoup(response.content, 'html.parser')
```

## Troubleshooting

### Authentication Issues
- Ensure credentials.json or client_secrets.json is in the project root
- Check that Google Sheets API is enabled in Google Cloud Console
- For OAuth2, delete token.pickle and re-authenticate

### Data Not Updating
- Verify internet connection
- Check NSE API/website availability
- Review script logs for errors

### Permission Denied
- Ensure service account email has access to the Google Sheet
- Or grant access via shared link in OAuth2 flow

## Project Structure

```
National-stock-exchange-/
├── nse_fno_tracker.py          # Main script
├── requirements.txt             # Python dependencies
├── setup_credentials.md         # Credential setup guide
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## Output Example

When you run the script, you'll see:

```
============================================================
NSE FNO Stocks to Google Sheets with Buy/Sell Signals
============================================================
✓ Google Sheets authenticated successfully

📊 Fetching NSE FNO data...
✓ Fetched 18 stocks

📝 Writing data to Google Sheet...
✓ Wrote 18 rows to sheet

🎨 Applying color formatting and conditional rules...
✓ Formatting applied successfully
  - Green highlight for BUY signals
  - Red highlight for SELL signals
  - Yellow highlight for HOLD signals
  - Green background for positive changes
  - Red background for negative changes

============================================================
✓ SUCCESS: All data written to Google Sheet with formatting
============================================================

📊 Open your sheet here:
https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID
```

## Support & Contributions

For issues, suggestions, or contributions, please open an issue or PR in this repository.

## License

MIT License - Feel free to use and modify

## Disclaimer

**Important**: This tool is for informational purposes only. The buy/sell signals are based on simple technical analysis and should NOT be considered as financial advice. Always conduct your own research and consult with a financial advisor before making investment decisions.
