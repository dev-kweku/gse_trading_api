import pandas as pd
from typing import List,Dist,Tuple
from datatime import datetime



def load_data(file_path:str)->pd.DataFrame:
    """Load CSV data into a pandas Dataframe with preprocessing"""

    df=pd.read_csv(file_path,sep="|",header=None,skiprows=1)

        # Set column names
    columns = [
        'index', 'daily_date', 'share_code', 'year_high', 'year_low', 
        'prev_closing_price', 'opening_price', 'last_transaction_price', 
        'closing_price', 'price_change', 'closing_bid_price', 
        'closing_offer_price', 'total_shares_traded', 'total_value_traded', 
        'scraped_date'
    ]
    df.columns = columns

    # clean data
    df=df[df['share_code']!= 'Daily Date']
    df=df.dropna(subset=['share_code'])

    df['daily_date']=pd.to_datetime(df['daily_date'],errors='coerce')
    df['scraped_date']=pd.to_datetime(df['scraped_date'],errors='coerce')


        # Convert numeric columns
    numeric_cols = [
        'year_high', 'year_low', 'prev_closing_price', 'opening_price',
        'last_transaction_price', 'closing_price', 'price_change',
        'closing_bid_price', 'closing_offer_price', 'total_shares_traded',
        'total_value_traded'
    ]

    for col in numeric_cols:
        df[col]=pd.to_numeric(df[col],errors='coerce')

    return df

def calculate_market_summary(df:pd.DataFrame,date:datetime.date)->Dict:
    """Calculate market summary for a specific date"""

    date_df=df[df['daily_date']== pd.to_datetime(date)]

    if date_df.empty:
        return{
            "date":date,
            "total_stocks":0,
            "total_value_traded":0,
            "total_shares_traded":0,
            "gainers":[],
            "losers":[],
            "most_active":[]
        }


    total_value=date_df['total_value_traded'].sum()
    total_shares=date_df['total_shares_traded'].sum()
    total_stocks=len(date_df)


    date_df=date_df.dropna(subset=['price_change'])
    gainers=date_df[date_df['price_change']>0].sort_values('price_change',ascending=False).head(5)
    losers=date_df[date_df['price_change']<0].sort_values('price_change').head(5)


    most_active=date_df.sort_values('total_value_traded',ascending=False).head(5)

    
    return {
        "date": date,
        "total_stocks": total_stocks,
        "total_value_traded": float(total_value),
        "total_shares_traded": int(total_shares),
        "gainers": gainers[['share_code', 'price_change']].to_dict('records'),
        "losers": losers[['share_code', 'price_change']].to_dict('records'),
        "most_active": most_active[['share_code', 'total_value_traded']].to_dict('records')
    }


def get_stock_history(df:pd.DataFrame,share_code:str)->List[Dict]:
    """get historical data for a specific stock"""

    stock_df=df[df['share_code']==share_code].sort_values('daily_date')

    history=[]
    for _,row in stock_df.iterrows():
        history.append({
            "daily_date": row['daily_date'].date(),
            "share_code": row['share_code'],
            "opening_price": row['opening_price'],
            "closing_price": row['closing_price'],
            "price_change": row['price_change'],
            "total_shares_traded": row['total_shares_traded'],
            "total_value_traded": row['total_value_traded']
        })

    return history