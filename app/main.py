import os
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core import config
from app.api import endpoints
from app.api.models import StockData

app = FastAPI(
    title=config.settings.PROJECT_NAME,
    openapi_url=f"{config.settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
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
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Get the project root directory (parent of app directory)
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
    
    print(f"Loaded {len(df)} rows from CSV")
    
    db = SessionLocal()
    
    # Check if data already exists
    existing_count = db.query(StockData).count()
    print(f"Existing records in database: {existing_count}")
    
    if existing_count == 0:
        # Import data
        success_count = 0
        error_count = 0
        
        for index, row in df.iterrows():
            try:
                # Skip rows with missing daily_date (should already be filtered in load_data, but double-check)
                if pd.isna(row['daily_date']):
                    print(f"Skipping row {index}: missing daily_date")
                    error_count += 1
                    continue
                
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
                success_count += 1
                
                # Print progress every 1000 records
                if success_count % 1000 == 0:
                    print(f"Processed {success_count} records successfully")
                    
            except Exception as e:
                print(f"Error processing row {index}: {e}")
                error_count += 1
        
        print(f"Data import completed: {success_count} records imported successfully, {error_count} errors")
    else:
        print("Data already exists in the database")
    
    # Verify the count after import
    final_count = db.query(StockData).count()
    print(f"Final record count in database: {final_count}")
    
    db.close()

@app.on_event("startup")
async def startup_event():
    init_db()