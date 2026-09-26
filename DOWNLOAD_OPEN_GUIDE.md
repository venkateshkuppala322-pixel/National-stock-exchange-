# Quick Start Guide - Download & Open NSE FNO Data

## Option 1: Export to Excel (Easiest)

### Step 1: Run the export script
```bash
pip install -r requirements_export.txt
python export_nse_data.py
```

### Step 2: Download the files
Two files will be created:
- `NSE_FNO_Stocks_YYYYMMDD_HHMMSS.xlsx` (Excel with color formatting)
- `NSE_FNO_Stocks_YYYYMMDD_HHMMSS.csv` (CSV file)

### Step 3: Open the Excel file
- Double-click the `.xlsx` file
- It opens in Excel, Google Sheets, or LibreOffice with all formatting

---

## Option 2: Import to Google Sheets (Free)

### Step 1: Create a Google Sheet
1. Go to https://sheets.google.com
2. Click **"+ New"** → **"Spreadsheet"**
3. Give it a name (e.g., "NSE FNO Tracker")

### Step 2: Run export script
```bash
python export_nse_data.py
```

### Step 3: Import CSV to Google Sheets
1. In Google Sheets, click **File** → **Import**
2. Select **"Upload"** tab
3. Upload the `.csv` file
4. Click **"Import data"**
5. Done! Your data is now in Google Sheets

### Step 4: Add formatting (Optional)
Google Sheets doesn't auto-apply color formatting from CSV. If you want colors:
1. Use the Excel file instead (it has all colors)
2. Or copy-paste from Excel and Google Sheets will preserve formatting

---

## Option 3: Use Both Files

- **Excel file (.xlsx)**: Full color formatting, ready to view
- **CSV file (.csv)**: Import to Google Sheets, plain text format

---

## File Contents

### Columns in the data:
| Column | Description |
|--------|-------------|
| Symbol | Stock ticker (RELIANCE, TCS, etc.) |
| LTP | Last Traded Price |
| High | Day's high price |
| Low | Day's low price |
| Close | Closing price |
| Change % | Percentage change from previous close |
| Trend | UP or DOWN |
| Signal | BUY, SELL, or HOLD |
| Volume | Trading volume |

### Color Coding:
- **🟢 GREEN**: BUY signals (Price up + positive trend)
- **🔴 RED**: SELL signals (Price down + negative trend)
- **🟡 YELLOW**: HOLD signals (Neutral)
- Light green background = Positive price change
- Light red background = Negative price change
- **BLUE**: UP trend
- **ORANGE**: DOWN trend

---

## Sharing Your Data

Once in Google Sheets:
1. Click **Share** (top right)
2. Enter email addresses or get a shareable link
3. Set permissions (Viewer/Commenter/Editor)
4. Send the link to team members

---

## Updating Data Regularly

### Automate daily updates:

#### Windows (Task Scheduler):
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at 9 AM
4. Set action: Run `python.exe C:\path\to\export_nse_data.py`
5. Enable "Run with highest privileges"

#### Mac/Linux (Crontab):
```bash
crontab -e

# Add this line for daily 9 AM run:
0 9 * * * cd /path/to/repo && python export_nse_data.py
```

---

## Troubleshooting

### Error: "No module named 'openpyxl'"
```bash
pip install -r requirements_export.txt
```

### Excel file won't open
- Try opening with Google Sheets or LibreOffice
- Ensure you have Excel or compatible software installed

### CSV import to Google Sheets shows wrong formatting
- Use the Excel file instead (better formatting support)
- Or manually apply colors in Google Sheets

---

## Example Output

After running the script, you'll see:
```
============================================================
NSE FNO STOCKS DATA - CSV & EXCEL EXPORT
============================================================
✓ Generated data for 18 stocks
✓ Displaying data...
...
✓ Excel file created: NSE_FNO_Stocks_20260926_084107.xlsx
✓ CSV file created: NSE_FNO_Stocks_20260926_084107.csv

✓ SUCCESS: Files created and ready for download

📥 Download these files:
  1️⃣  Excel (with color formatting): NSE_FNO_Stocks_20260926_084107.xlsx
  2️⃣  CSV (for Google Sheets import): NSE_FNO_Stocks_20260926_084107.csv
```

---

## Next Steps

✅ Download the Excel file  
✅ Open in Excel or Google Sheets  
✅ Share with team members  
✅ Set up daily automatic updates  
