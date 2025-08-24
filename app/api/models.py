from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from sqlalchemy.types import Integer as SQLAlchemyInteger
from app.core.database import Base

class StockData(Base):
    __tablename__ = "stock_data"
    
    id = Column(Integer, primary_key=True, index=True)
    daily_date = Column(Date, nullable=False, index=True)
    share_code = Column(String(50), nullable=False, index=True)
    year_high = Column(Float)
    year_low = Column(Float)
    prev_closing_price = Column(Float)
    opening_price = Column(Float)
    last_transaction_price = Column(Float)
    closing_price = Column(Float)
    price_change = Column(Float)
    closing_bid_price = Column(Float)
    closing_offer_price = Column(Float)
    total_shares_traded = Column(SQLAlchemyInteger) 
    total_value_traded = Column(Float)
    scraped_date = Column(DateTime)