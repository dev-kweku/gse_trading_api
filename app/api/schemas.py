from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class StockDataBase(BaseModel):
    daily_date: date
    share_code: str
    year_high: Optional[float] = None
    year_low: Optional[float] = None
    prev_closing_price: Optional[float] = None
    opening_price: Optional[float] = None
    last_transaction_price: Optional[float] = None
    closing_price: Optional[float] = None
    price_change: Optional[float] = None
    closing_bid_price: Optional[float] = None
    closing_offer_price: Optional[float] = None
    total_shares_traded: Optional[int] = None  
    total_value_traded: Optional[float] = None
    scraped_date: Optional[datetime] = None

class StockDataCreate(StockDataBase):
    pass

class StockDataUpdate(StockDataBase):
    pass

class StockDataInDBBase(StockDataBase):
    id: int
    
    class Config:
        from_attributes = True

class StockData(StockDataInDBBase):
    pass

class MarketSummary(BaseModel):
    date: date
    total_stocks: int
    total_value_traded: float
    total_shares_traded: int
    gainers: List[dict]
    losers: List[dict]
    most_active: List[dict]

class StockHistory(BaseModel):
    share_code: str
    history: List[StockData]
    
    class Config:
        from_attributes = True