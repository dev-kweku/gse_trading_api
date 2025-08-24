from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
from app.core.database import get_db
from app.api import schemas
from app.crud import stock_crud
from app.data.processor import load_data, calculate_market_summary, get_stock_history
from app.core.config import settings
from app.api.models import StockData  

router = APIRouter()


df = load_data(settings.DATA_FILE_PATH)

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
def get_stock_history_endpoint(share_code: str):
    """
    Get historical data for a specific stock.
    """
    history = get_stock_history(df, share_code)
    if not history:
        raise HTTPException(status_code=404, detail=f"No history found for share code: {share_code}")
    
    return {
        "share_code": share_code,
        "history": history
    }

@router.get("/market/summary/{date}", response_model=schemas.MarketSummary)
def get_market_summary(date: date):
    """
    Get market summary for a specific date.
    """
    summary = calculate_market_summary(df, date)
    return summary

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