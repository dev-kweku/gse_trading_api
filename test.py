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
    if data:  
        assert data[0]["share_code"] == share_code

#will add more test

if __name__ == "__main__":
    test_get_stocks()
    test_get_stocks_by_code()
    print("All tests passed!")