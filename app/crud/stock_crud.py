from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.models import StockData
from app.api.schemas import StockDataCreate, StockDataUpdate

def get_stock_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(StockData).offset(skip).limit(limit).all()

def get_stock_data_by_id(db: Session, id: int):
    return db.query(StockData).filter(StockData.id == id).first()

def get_stock_data_by_code(db: Session, share_code: str):
    return db.query(StockData).filter(StockData.share_code == share_code).all()

def get_stock_data_by_date(db: Session, daily_date: str):
    return db.query(StockData).filter(StockData.daily_date == daily_date).all()

def create_stock_data(db: Session, stock: StockDataCreate):
    try:
        db_stock = StockData(**stock.dict())
        db.add(db_stock)
        db.commit()
        db.refresh(db_stock)
        return db_stock
    except Exception as e:
        db.rollback()
        print(f"Error creating stock data: {e}")
        raise e

def update_stock_data(db: Session, id: int, stock: StockDataUpdate):
    db_stock = db.query(StockData).filter(StockData.id == id).first()
    if db_stock:
        for key, value in stock.dict(exclude_unset=True).items():
            setattr(db_stock, key, value)
        db.commit()
        db.refresh(db_stock)
    return db_stock

def delete_stock_data(db: Session, id: int):
    db_stock = db.query(StockData).filter(StockData.id == id).first()
    if db_stock:
        db.delete(db_stock)
        db.commit()
    return db_stock