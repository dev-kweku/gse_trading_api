import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core import config
from app.api import endpoints
from app.api.models import StockData

app = FastAPI(
    title=config.settings.PROJECT_NAME,
    openapi_url=f"{config.settings.API_V1_STR}/openapi.json"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(endpoints.router, prefix=config.settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to GSE Trading Data API"}

def init_db():
    """Initialize the database with data from CSV if needed."""
    from app.core.database import engine, SessionLocal
    from app.api.models import Base
    from app.data.processor import load_data
    from app.api.schemas import StockDataCreate
    from app.crud import stock_crud
    
    
    Base.metadata.create_all(bind=engine)
    
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file_path = os.path.join(project_root, config.settings.DATA_FILE_PATH)
    
    print(f"Project root: {project_root}")
    print(f"Attempting to load data from: {data_file_path}")
    
    if not os.path.exists(data_file_path):
        print(f"Error: Data file not found at {data_file_path}")
        print(f"Current working directory: {os.getcwd()}")
        data_dir = os.path.join(project_root, "data")
        print(f"Data directory: {data_dir}")
        print(f"Files in data directory: {os.listdir(data_dir) if os.path.exists(data_dir) else 'Data directory not found'}")
        return
    
    # Load data from CSV
    df = load_data(data_file_path)
    if df.empty:
        print("Warning: No data loaded from CSV")
        return
    
    db = SessionLocal()
    
    # Check if data already exists
    if db.query(StockData).count() == 0:
        # Import data
        for _, row in df.iterrows():
            stock_data = StockDataCreate(
                daily_date=row['daily_date'].date(),
                share_code=row['share_code'],
                year_high=row['year_high'],
                year_low=row['year_low'],
                prev_closing_price=row['prev_closing_price'],
                opening_price=row['opening_price'],
                last_transaction_price=row['last_transaction_price'],
                closing_price=row['closing_price'],
                price_change=row['price_change'],
                closing_bid_price=row['closing_bid_price'],
                closing_offer_price=row['closing_offer_price'],
                total_shares_traded=row['total_shares_traded'],
                total_value_traded=row['total_value_traded'],
                scraped_date=row['scraped_date']
            )
            stock_crud.create_stock_data(db, stock_data)
        print("Data imported successfully")
    else:
        print("Data already exists in the database")
    
    db.close()

@app.on_event("startup")
async def startup_event():
    init_db()