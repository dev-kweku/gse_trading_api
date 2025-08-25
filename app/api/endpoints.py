from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
from app.core.database import get_db
from app.api import schemas
from app.crud import stock_crud
from app.api.models import StockData
from app.core.config import settings

router = APIRouter()

@router.get("/stocks", response_model=List[schemas.StockData])
def get_stocks(
    skip: int = 0,
    limit: int = 100,
    share_code: Optional[str] = Query(None, description="Filter by share code"),
    start_date: Optional[date] = Query(None, description="Filter by start date"),
    end_date: Optional[date] = Query(None, description="Filter by end date"),
    db: Session = Depends(get_db)
):
    """
    Retrieve stock data with optional filtering.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **share_code**: Filter by specific share code
    - **start_date**: Filter by start date (inclusive)
    - **end_date**: Filter by end date (inclusive)
    """
    query = db.query(StockData)
    
    if share_code:
        query = query.filter(StockData.share_code == share_code)
    
    if start_date:
        query = query.filter(StockData.daily_date >= start_date)
    
    if end_date:
        query = query.filter(StockData.daily_date <= end_date)
    
    stocks = query.offset(skip).limit(limit).all()
    return stocks

@router.get("/stocks/{stock_id}", response_model=schemas.StockData)
def get_stock(stock_id: int, db: Session = Depends(get_db)):
    """
    Get a specific stock by ID.
    """
    stock = stock_crud.get_stock_data_by_id(db, stock_id=stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock

@router.get("/stocks/code/{share_code}", response_model=List[schemas.StockData])
def get_stock_by_code(share_code: str, db: Session = Depends(get_db)):
    """
    Get all records for a specific share code.
    """
    stocks = stock_crud.get_stock_data_by_code(db, share_code=share_code)
    if not stocks:
        raise HTTPException(status_code=404, detail=f"No data found for share code: {share_code}")
    return stocks

@router.get("/stocks/date/{daily_date}", response_model=List[schemas.StockData])
def get_stocks_by_date(daily_date: date, db: Session = Depends(get_db)):
    """
    Get all stocks for a specific date.
    """
    stocks = stock_crud.get_stock_data_by_date(db, daily_date=daily_date)
    if not stocks:
        raise HTTPException(status_code=404, detail=f"No data found for date: {daily_date}")
    return stocks

@router.get("/stocks/{share_code}/history", response_model=schemas.StockHistory)
def get_stock_history_endpoint(share_code: str, db: Session = Depends(get_db)):
    """
    Get historical data for a specific stock.
    """
    # Query the database for the stock history
    stock_records = db.query(StockData).filter(StockData.share_code == share_code).order_by(StockData.daily_date).all()
    
    if not stock_records:
        raise HTTPException(status_code=404, detail=f"No history found for share code: {share_code}")
    
    history = []
    for record in stock_records:
        history.append({
            "daily_date": record.daily_date,
            "share_code": record.share_code,
            "opening_price": record.opening_price,
            "closing_price": record.closing_price,
            "price_change": record.price_change,
            "total_shares_traded": record.total_shares_traded,
            "total_value_traded": record.total_value_traded
        })
    
    return {
        "share_code": share_code,
        "history": history
    }

@router.get("/market/summary/{date}", response_model=schemas.MarketSummary)
def get_market_summary(date: date, db: Session = Depends(get_db)):
    """
    Get market summary for a specific date.
    """
    # Get all stocks for the specified date
    stocks = db.query(StockData).filter(StockData.daily_date == date).all()
    
    if not stocks:
        return {
            "date": date,
            "total_stocks": 0,
            "total_value_traded": 0,
            "total_shares_traded": 0,
            "gainers": [],
            "losers": [],
            "most_active": []
        }
    
    # Calculate totals
    total_value = sum(stock.total_value_traded or 0 for stock in stocks)
    total_shares = sum(stock.total_shares_traded or 0 for stock in stocks)
    total_stocks = len(stocks)
    
    # Find gainers and losers
    gainers = []
    losers = []
    
    for stock in stocks:
        if stock.price_change is not None:
            if stock.price_change > 0:
                gainers.append({
                    "share_code": stock.share_code,
                    "price_change": stock.price_change
                })
            elif stock.price_change < 0:
                losers.append({
                    "share_code": stock.share_code,
                    "price_change": stock.price_change
                })
    
    # Sort gainers and losers
    gainers = sorted(gainers, key=lambda x: x["price_change"], reverse=True)[:5]
    losers = sorted(losers, key=lambda x: x["price_change"])[:5]
    
    # Find most active stocks by value traded
    most_active = []
    for stock in stocks:
        most_active.append({
            "share_code": stock.share_code,
            "total_value_traded": stock.total_value_traded or 0
        })
    
    most_active = sorted(most_active, key=lambda x: x["total_value_traded"], reverse=True)[:5]
    
    return {
        "date": date,
        "total_stocks": total_stocks,
        "total_value_traded": float(total_value),
        "total_shares_traded": int(total_shares),
        "gainers": gainers,
        "losers": losers,
        "most_active": most_active
    }

@router.get("/stocks/count")
def get_stocks_count(db: Session = Depends(get_db)):
    """Get the total count of stock records in the database."""
    count = db.query(StockData).count()
    return {"count": count}

@router.get("/stocks/all", response_model=List[schemas.StockData])
def get_all_stocks(db: Session = Depends(get_db)):
    """Get all stock records without pagination."""
    stocks = db.query(StockData).all()
    return stocks

@router.post("/stocks", response_model=schemas.StockData)
def create_stock(stock: schemas.StockDataCreate, db: Session = Depends(get_db)):
    """
    Create a new stock record.
    """
    return stock_crud.create_stock_data(db=db, stock=stock)

@router.put("/stocks/{stock_id}", response_model=schemas.StockData)
def update_stock(stock_id: int, stock: schemas.StockDataUpdate, db: Session = Depends(get_db)):
    """
    Update a stock record.
    """
    db_stock = stock_crud.update_stock_data(db=db, id=stock_id, stock=stock)
    if not db_stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return db_stock

@router.delete("/stocks/{stock_id}")
def delete_stock(stock_id: int, db: Session = Depends(get_db)):
    """
    Delete a stock record.
    """
    db_stock = stock_crud.delete_stock_data(db=db, id=stock_id)
    if not db_stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return {"message": "Stock deleted successfully"}