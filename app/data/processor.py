import pandas as pd
from typing import List, Dict, Tuple
from datetime import datetime
import os
import numpy as np

def load_data(file_path: str) -> pd.DataFrame:
    """Load CSV data into a pandas DataFrame with preprocessing."""
    try:
        print(f"Loading data from: {file_path}")
        
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            return pd.DataFrame()
        
        # Read the first line to understand the structure
        with open(file_path, 'r') as f:
            first_line = f.readline().strip()
            print(f"First line: {first_line}")
        
        # Read CSV with comma delimiter, using the first row as header
        df = pd.read_csv(file_path, header=0)
        
        print(f"Initial DataFrame shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        # Clean data
        df = df[df['Share Code'] != 'Daily Date']  # Remove header rows
        df = df.dropna(subset=['Share Code'])  # Remove rows with missing share code
        
        print(f"After cleaning: {df.shape}")
        
        # Rename columns to match our schema
        column_mapping = {
            'Daily Date': 'daily_date',
            'Share Code': 'share_code',
            'Year High (GH¢)': 'year_high',
            'Year Low (GH¢)': 'year_low',
            'Previous Closing Price - VWAP (GH¢)': 'prev_closing_price',
            'Opening Price (GH¢)': 'opening_price',
            'Last Transaction Price (GH¢)': 'last_transaction_price',
            'Closing Price - VWAP (GH¢)': 'closing_price',
            'Price Change (GH¢)': 'price_change',
            'Closing Bid Price (GH¢)': 'closing_bid_price',
            'Closing Offer Price (GH¢)': 'closing_offer_price',
            'Total Shares Traded': 'total_shares_traded',
            'Total Value Traded (GH¢)': 'total_value_traded',
            'Scraped_Date': 'scraped_date'
        }
        
        df = df.rename(columns=column_mapping)
        
        # Convert data types
        # Fix date parsing by specifying dayfirst=True for DD/MM/YYYY format
        df['daily_date'] = pd.to_datetime(df['daily_date'], dayfirst=True, errors='coerce')
        df['scraped_date'] = pd.to_datetime(df['scraped_date'], errors='coerce')
        
        # Convert numeric columns
        numeric_cols = [
            'year_high', 'year_low', 'prev_closing_price', 'opening_price',
            'last_transaction_price', 'closing_price', 'price_change',
            'closing_bid_price', 'closing_offer_price', 'total_value_traded'
        ]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Convert total_shares_traded to integer, handling fractional values
        df['total_shares_traded'] = pd.to_numeric(df['total_shares_traded'], errors='coerce')
        # Round fractional shares to the nearest integer
        df['total_shares_traded'] = df['total_shares_traded'].round().astype('Int64')  # Int64 supports NaN
        
        # Remove rows with missing daily_date (required field)
        initial_count = len(df)
        df = df.dropna(subset=['daily_date'])
        final_count = len(df)
        
        if initial_count != final_count:
            print(f"Removed {initial_count - final_count} rows with missing daily_date")
        
        print(f"Final DataFrame shape: {df.shape}")
        print(f"Sample data:\n{df.head()}")
        
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def calculate_market_summary(df: pd.DataFrame, date: datetime.date) -> Dict:
    """Calculate market summary for a specific date."""
    try:
        date_df = df[df['daily_date'] == pd.to_datetime(date)]
        
        if date_df.empty:
            return {
                "date": date,
                "total_stocks": 0,
                "total_value_traded": 0,
                "total_shares_traded": 0,
                "gainers": [],
                "losers": [],
                "most_active": []
            }
        
        
        total_value = date_df['total_value_traded'].sum()
        total_shares = date_df['total_shares_traded'].sum()
        total_stocks = len(date_df)
        
        
        date_df = date_df.dropna(subset=['price_change'])
        gainers = date_df[date_df['price_change'] > 0].sort_values('price_change', ascending=False).head(5)
        losers = date_df[date_df['price_change'] < 0].sort_values('price_change').head(5)
        
    
        most_active = date_df.sort_values('total_value_traded', ascending=False).head(5)
        
        return {
            "date": date,
            "total_stocks": total_stocks,
            "total_value_traded": float(total_value),
            "total_shares_traded": int(total_shares) if not pd.isna(total_shares) else 0,
            "gainers": gainers[['share_code', 'price_change']].to_dict('records'),
            "losers": losers[['share_code', 'price_change']].to_dict('records'),
            "most_active": most_active[['share_code', 'total_value_traded']].to_dict('records')
        }
    except Exception as e:
        print(f"Error calculating market summary: {e}")
        return {
            "date": date,
            "total_stocks": 0,
            "total_value_traded": 0,
            "total_shares_traded": 0,
            "gainers": [],
            "losers": [],
            "most_active": []
        }

def get_stock_history(df: pd.DataFrame, share_code: str) -> List[Dict]:
    """Get historical data for a specific stock."""
    try:
        stock_df = df[df['share_code'] == share_code].sort_values('daily_date')
        
        
        history = []
        for _, row in stock_df.iterrows():
            history.append({
                "daily_date": row['daily_date'].date() if pd.notna(row['daily_date']) else None,
                "share_code": row['share_code'],
                "opening_price": row['opening_price'],
                "closing_price": row['closing_price'],
                "price_change": row['price_change'],
                "total_shares_traded": int(row['total_shares_traded']) if not pd.isna(row['total_shares_traded']) else 0,
                "total_value_traded": row['total_value_traded']
            })
        
        return history
    except Exception as e:
        print(f"Error getting stock history: {e}")
        return []