

# GSE Trading Data API

A comprehensive REST API for accessing and analyzing Ghana Stock Exchange (GSE) trading data. Built with FastAPI, this API provides endpoints for retrieving stock data, market summaries, and historical information.

## Features

- Access to daily stock trading data
- Historical data for individual stocks
- Market summaries for specific dates
- Filtering by date range and share code
- CRUD operations for stock data
- Interactive API documentation
- CORS enabled for web application integration

## Installation

### Prerequisites

- Python 3.8+
- pip package manager
- SQLite (included with Python)

### Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd gse-trading-api
```

2. Create a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Place your CSV data file in the `data/` directory:
```
gse-trading-api/
├── data/
│   └── gse_trading_data_full_20250823_183328.csv
```

5. Run the application:
```bash
python run.py
```

The API will be available at http://localhost:8000.

### Production Setup

1. Set up a server (Ubuntu recommended)
2. Install Docker and Docker Compose
3. Clone the repository on the server
4. Create a `.env` file with production settings:
```
DATABASE_URL=sqlite:///./gse_trading.db
DATA_FILE_PATH=/app/data/gse_trading_data_full_20250823_183328.csv
SECRET_KEY=your-secret-key-here
```
5. Build and run with Docker Compose:
```bash
docker-compose up -d --build
```

6. Set up Nginx as a reverse proxy and SSL with Let's Encrypt

## Project Structure

```
gse-trading-api/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints.py       # API route definitions
│   │   ├── models.py          # SQLAlchemy models
│   │   └── schemas.py         # Pydantic models for validation
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration settings
│   │   └── database.py        # Database connection setup
│   ├── crud/
│   │   ├── __init__.py
│   │   └── stock_crud.py      # CRUD operations
│   ├── data/
│   │   ├── __init__.py
│   │   └── processor.py       # Data processing utilities
│   └── main.py                # FastAPI application entry point
├── data/
│   └── gse_trading_data_full_20250823_183328.csv
├── requirements.txt
├── run.py                     # Script to run the application
└── README.md                  # This file
```

## API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Endpoints

#### Get Stocks
Retrieve stock data with optional filtering.

```
GET /stocks
```

Parameters:
- `skip`: Number of records to skip (for pagination)
- `limit`: Maximum number of records to return
- `share_code`: Filter by specific share code
- `start_date`: Filter by start date (inclusive)
- `end_date`: Filter by end date (inclusive)

Example:
```bash
curl -X GET "http://localhost:8000/api/v1/stocks?limit=100"
```

#### Get Stock by ID
Get a specific stock by ID.

```
GET /stocks/{stock_id}
```

Example:
```bash
curl -X GET "http://localhost:8000/api/v1/stocks/1"
```

#### Get Stock by Share Code
Get all records for a specific share code.

```
GET /stocks/code/{share_code}
```

Example:
```bash
curl -X GET "http://localhost:8000/api/v1/stocks/code/MTNGH"
```

#### Get Stocks by Date
Get all stocks for a specific date.

```
GET /stocks/date/{daily_date}
```

Example:
```bash
curl -X GET "http://localhost:8000/api/v1/stocks/date/2025-08-22"
```

#### Get Stock History
Get historical data for a specific stock.

```
GET /stocks/{share_code}/history
```

Example:
```bash
curl -X GET "http://localhost:8000/api/v1/stocks/MTNGH/history"
```

#### Get Market Summary
Get market summary for a specific date.

```
GET /market/summary/{date}
```

Example:
```bash
curl -X GET "http://localhost:8000/api/v1/market/summary/2025-08-22"
```

#### Get Stock Count
Get the total count of stock records in the database.

```
GET /stocks/count
```

Example:
```bash
curl -X GET "http://localhost:8000/api/v1/stocks/count"
```

#### Get All Stocks
Get all stock records without pagination.

```
GET /stocks/all
```

Example:
```bash
curl -X GET "http://localhost:8000/api/v1/stocks/all"
```

#### Create Stock
Create a new stock record.

```
POST /stocks
```

Request Body:
```json
{
  "daily_date": "2025-08-23",
  "share_code": "TEST",
  "year_high": 10.0,
  "year_low": 5.0,
  "prev_closing_price": 8.0,
  "opening_price": 8.0,
  "last_transaction_price": 8.5,
  "closing_price": 8.5,
  "price_change": 0.5,
  "closing_bid_price": 8.4,
  "closing_offer_price": 8.6,
  "total_shares_traded": 1000,
  "total_value_traded": 8500.0,
  "scraped_date": "2025-08-23T18:33:27"
}
```

Example:
```bash
curl -X POST "http://localhost:8000/api/v1/stocks" \
-H "Content-Type: application/json" \
-d '{
  "daily_date": "2025-08-23",
  "share_code": "TEST",
  "year_high": 10.0,
  "year_low": 5.0,
  "prev_closing_price": 8.0,
  "opening_price": 8.0,
  "last_transaction_price": 8.5,
  "closing_price": 8.5,
  "price_change": 0.5,
  "closing_bid_price": 8.4,
  "closing_offer_price": 8.6,
  "total_shares_traded": 1000,
  "total_value_traded": 8500.0,
  "scraped_date": "2025-08-23T18:33:27"
}'
```

#### Update Stock
Update a stock record.

```
PUT /stocks/{stock_id}
```

Request Body:
```json
{
  "closing_price": 9.0,
  "price_change": 1.0
}
```

Example:
```bash
curl -X PUT "http://localhost:8000/api/v1/stocks/1" \
-H "Content-Type: application/json" \
-d '{
  "closing_price": 9.0,
  "price_change": 1.0
}'
```

#### Delete Stock
Delete a stock record.

```
DELETE /stocks/{stock_id}
```

Example:
```bash
curl -X DELETE "http://localhost:8000/api/v1/stocks/1"
```

### Interactive Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Running the Application

### Development Server

1. Activate your virtual environment:
```bash
source env/bin/activate  # On Windows: env\Scripts\activate
```

2. Run the application:
```bash
python run.py
```

The API will be available at http://localhost:8000.

### Using Docker

1. Build the Docker image:
```bash
docker build -t gse-trading-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 -v $(pwd)/data:/app/data gse-trading-api
```

### Using Docker Compose

1. Run with Docker Compose:
```bash
docker-compose up -d
```

## Testing the API

### Using curl Commands

See the examples in the API Endpoints section above.

### Using Python Requests Library

Create a Python script to test the API:

```python
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_get_stocks():
    response = requests.get(f"{BASE_URL}/stocks")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_get_stocks_by_code():
    share_code = "MTNGH"
    response = requests.get(f"{BASE_URL}/stocks/code/{share_code}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

# Add more test functions as needed

if __name__ == "__main__":
    test_get_stocks()
    test_get_stocks_by_code()
```

### Using FastAPI's TestClient

Create a file `test_api.py`:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_stocks():
    response = client.get("/api/v1/stocks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_stocks_by_code():
    share_code = "MTNGH"
    response = client.get(f"/api/v1/stocks/code/{share_code}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:  # If there's data
        assert data[0]["share_code"] == share_code

# Add more test functions as needed

if __name__ == "__main__":
    test_get_stocks()
    test_get_stocks_by_code()
    print("All tests passed!")
```

Run the tests:
```bash
python test_api.py
```

## Deployment

### Using Docker

1. Build the Docker image:
```bash
docker build -t gse-trading-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 -v $(pwd)/data:/app/data gse-trading-api
```

### Using Docker Compose

1. Create a `docker-compose.yml` file:
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

2. Run with Docker Compose:
```bash
docker-compose up -d
```

### Cloud Deployment

For production deployment to cloud platforms like AWS, Google Cloud, or Azure, refer to the hosting guide in the project documentation.

## Troubleshooting

### Common Issues

1. **Pydantic Import Error**
   - If you encounter an error about `BaseSettings` not being found, install `pydantic-settings`:
   ```bash
   pip install pydantic-settings
   ```

2. **Data Loading Issues**
   - If the API returns only a few records or no records, check the following:
     - Ensure the CSV file is in the correct location (`data/` directory)
     - Verify the file path in `app/core/config.py`
     - Check the server logs for any errors during data loading
     - Try deleting the database file (`gse_trading.db`) and restarting the server

3. **Date Validation Error**
   - If you encounter errors about invalid dates, ensure that:
     - All rows in the CSV have valid dates in the `Daily Date` column
     - The date format is consistent (DD/MM/YYYY)

4. **Database Connection Issues**
   - If you encounter database connection errors, ensure that:
     - The database file (`gse_trading.db`) is not being used by another process
     - You have write permissions in the project directory

5. **CORS Issues**
   - If you encounter CORS errors when accessing the API from a web application:
     - Ensure the CORS middleware is properly configured in `app/main.py`
     - For production, update the `allow_origins` parameter to include your frontend domain

### Debugging

To enable more detailed logging, modify the `load_data` function in `app/data/processor.py` to print more information about the data loading process.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.