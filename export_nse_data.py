#!/usr/bin/env python3
"""
NSE FNO Stocks Data Export - Create and Download as CSV/Excel
"""

import pandas as pd
from datetime import datetime
import os

class NSEFNODataExport:
    def __init__(self):
        self.df = None
        self.filename_base = f"NSE_FNO_Stocks_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def generate_nse_fno_data(self):
        """
        Generate NSE FNO (Futures & Options) sample data
        """
        print("\n📊 Generating NSE FNO Stocks Data...")
        
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
        
        self.df = pd.DataFrame(fno_data)
        
        # Calculate technical indicators
        self.df['Change %'] = ((self.df['LTP'] - self.df['Prev Close']) / self.df['Prev Close'] * 100).round(2)
        self.df['SMA_20'] = self.df['Close'].rolling(window=3).mean()
        self.df['Trend'] = self.df['Close'].apply(lambda x: 'UP' if x > 2500 else 'DOWN')
        
        # Generate Buy/Sell signals
        self.df['Signal'] = self.df.apply(self.generate_signal, axis=1)
        
        print(f"✓ Generated data for {len(self.df)} stocks")
        return self.df

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

    def create_excel_with_formatting(self):
        """
        Create Excel file with color formatting
        """
        print("\n📝 Creating Excel file with color formatting...")
        
        excel_file = f"{self.filename_base}.xlsx"
        
        # Create Excel writer object
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            self.df.to_excel(writer, sheet_name='NSE FNO Data', index=False)
            
            # Get the workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets['NSE FNO Data']
            
            from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
            
            # Define colors
            green_fill = PatternFill(start_color="00B050", end_color="00B050", fill_type="solid")  # Green
            red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")    # Red
            yellow_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")  # Yellow
            light_green_fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
            light_red_fill = PatternFill(start_color="F8CECC", end_color="F8CECC", fill_type="solid")
            blue_fill = PatternFill(start_color="DDEBF7", end_color="DDEBF7", fill_type="solid")
            orange_fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
            header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")  # Dark Blue
            
            white_font = Font(bold=True, color="FFFFFF", size=11)
            green_font = Font(bold=True, color="008000")  # Dark Green
            red_font = Font(bold=True, color="FF0000")  # Red
            blue_font = Font(bold=True, color="0000FF")  # Blue
            
            # Format header row
            for cell in worksheet[1]:
                cell.fill = header_fill
                cell.font = white_font
                cell.alignment = Alignment(horizontal='center', vertical='center')
            
            # Set column widths
            column_widths = {'A': 12, 'B': 12, 'C': 12, 'D': 12, 'E': 12, 'F': 12, 'G': 12, 'H': 12, 'I': 15}
            for col, width in column_widths.items():
                worksheet.column_dimensions[col].width = width
            
            # Apply formatting to data rows
            for row_idx, row in enumerate(worksheet.iter_rows(min_row=2, max_row=len(self.df) + 1), start=2):
                # Column H = Signal (index 7)
                signal_cell = row[7]
                signal_value = signal_cell.value
                
                if signal_value == "BUY":
                    signal_cell.fill = green_fill
                    signal_cell.font = Font(bold=True, color="FFFFFF")
                elif signal_value == "SELL":
                    signal_cell.fill = red_fill
                    signal_cell.font = Font(bold=True, color="FFFFFF")
                elif signal_value == "HOLD":
                    signal_cell.fill = yellow_fill
                    signal_cell.font = Font(bold=True, color="000000")
                
                signal_cell.alignment = Alignment(horizontal='center', vertical='center')
                
                # Column F = Change % (index 5)
                change_cell = row[5]
                try:
                    change_val = float(str(change_cell.value).replace('%', ''))
                    if change_val > 0:
                        change_cell.fill = light_green_fill
                        change_cell.font = Font(color="008000", bold=True)
                    elif change_val < 0:
                        change_cell.fill = light_red_fill
                        change_cell.font = Font(color="FF0000", bold=True)
                except:
                    pass
                change_cell.alignment = Alignment(horizontal='center', vertical='center')
                
                # Column G = Trend (index 6)
                trend_cell = row[6]
                trend_value = trend_cell.value
                if trend_value == "UP":
                    trend_cell.fill = blue_fill
                    trend_cell.font = blue_font
                elif trend_value == "DOWN":
                    trend_cell.fill = orange_fill
                    trend_cell.font = Font(bold=True, color="FF6600")
                trend_cell.alignment = Alignment(horizontal='center', vertical='center')
                
                # Center align numeric columns
                for i in [0, 1, 2, 3, 4]:  # Symbol, LTP, High, Low, Close
                    row[i].alignment = Alignment(horizontal='center', vertical='center')
                row[8].alignment = Alignment(horizontal='right', vertical='center')  # Volume
        
        print(f"✓ Excel file created: {excel_file}")
        return excel_file

    def create_csv_file(self):
        """
        Create CSV file
        """
        print("\n📋 Creating CSV file...")
        
        csv_file = f"{self.filename_base}.csv"
        self.df.to_csv(csv_file, index=False)
        
        print(f"✓ CSV file created: {csv_file}")
        return csv_file

    def display_data(self):
        """
        Display data in terminal
        """
        print("\n" + "="*120)
        print("NSE FNO STOCKS DATA WITH BUY/SELL SIGNALS")
        print("="*120)
        print(self.df.to_string(index=False))
        print("="*120)
        print(f"\nTotal Records: {len(self.df)}")
        print(f"\nBUY Signals: {len(self.df[self.df['Signal'] == 'BUY'])}")
        print(f"SELL Signals: {len(self.df[self.df['Signal'] == 'SELL'])}")
        print(f"HOLD Signals: {len(self.df[self.df['Signal'] == 'HOLD'])}")

    def run(self):
        """
        Main execution flow
        """
        print("\n" + "="*120)
        print("NSE FNO STOCKS DATA - CSV & EXCEL EXPORT WITH BUY/SELL SIGNALS & COLOR FORMATTING")
        print("="*120)
        
        try:
            # Generate data
            self.generate_nse_fno_data()
            
            # Display data
            self.display_data()
            
            # Create Excel with formatting
            excel_file = self.create_excel_with_formatting()
            
            # Create CSV
            csv_file = self.create_csv_file()
            
            print("\n" + "="*120)
            print("✓ SUCCESS: Files created and ready for download")
            print("="*120)
            
            print(f"\n📥 Download these files:")
            print(f"  1️⃣  Excel (with color formatting): {excel_file}")
            print(f"  2️⃣  CSV (for Google Sheets import): {csv_file}")
            
            print(f"\n📊 To import to Google Sheets:")
            print(f"  1. Go to https://sheets.google.com")
            print(f"  2. Create a new spreadsheet")
            print(f"  3. Click 'File' → 'Import' → 'Upload'")
            print(f"  4. Select {csv_file}")
            print(f"  5. Click 'Import data'")
            print(f"\n  OR simply open {excel_file} in Excel/Google Sheets!")
            
            print(f"\n🎨 Color Legend:")
            print(f"  🟢 GREEN   = BUY Signal (Strong Uptrend)")
            print(f"  🔴 RED     = SELL Signal (Strong Downtrend)")
            print(f"  🟡 YELLOW  = HOLD Signal (Neutral)")
            print(f"  📈 BLUE    = UP Trend")
            print(f"  📉 ORANGE  = DOWN Trend")
            
            print(f"\n" + "="*120)
            
        except Exception as e:
            print(f"\n✗ FAILED: {e}")
            raise


if __name__ == "__main__":
    exporter = NSEFNODataExport()
    exporter.run()
