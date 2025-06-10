# Stock Portfolio API

This is a **FastAPI-based** API that provides stock portfolio data, including company names and current prices, by reading from a CSV file and fetching live data using Yahoo Finance.

## Features

- Reads stock holdings from `stocks.csv`
- Fetches company names and current prices using [yfinance](https://github.com/ranaroussi/yfinance)
- Caches results for efficiency
- CORS enabled for frontend integration
- Supports filtering by market, sector, and industry via query parameters
- Returns standardized JSON responses for easy integration

## Project Structure

```
stock-portfolio-api/
├── main.py           # Main FastAPI server
├── requirements.txt  # Python dependencies
├── stocks.csv        # Portfolio data (edit this file to update holdings)
└── .gitignore
```

## Setup

1. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare your portfolio data**

   Edit `stocks.csv` to include your holdings. Example format:

   ```
   market,symbol,currency,shares,avgCost
   US,AAPL,USD,10,150
   HK,0005.HK,HKD,500,60
   ```

3. **Run the API server**

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

   The API will be available at [http://localhost:8000/api/stocks](http://localhost:8000/api/stocks).

## API Endpoint

### `GET /api/stocks`

Returns a JSON array of your stock holdings with live company names and prices.

#### Query Parameters

- `market` (optional): Filter by market (e.g., `US`, `HK`)
- `sector` (optional): Filter by sector (e.g., `Energy`)
- `industry` (optional): Filter by industry
- `fields` (optional): Comma-separated list of fields to include in the response
- `sort_by` (optional): Field to sort the results by

**Example request:**

```
GET /api/stocks?market=US&sector=Technology&fields=market,symbol,company,currentPrice
```

**Example response:**

```json
{
  "data": [
    {
      "market": "US",
      "symbol": "AAPL",
      "company": "Apple Inc.",
      "currentPrice": 175.2
    }
  ],
  "metadata": {
    "request_id": "uuid",
    "timestamp": "2025-06-09T12:00:00Z",
    "status": "success",
    "endpoint": "get_stocks",
    "query_params": {
      "fields": "market,symbol,company,currentPrice",
      "market": "US",
      "sector": "Technology",
      "industry": null,
      "sort_by": null
    }
  },
  "errors": []
}
```

## Notes

- The API fetches live data from Yahoo Finance. If a symbol is invalid or data is unavailable, an error will be returned.
- The server uses an in-memory cache for efficiency. Restarting the server will clear the cache.

## Dependencies

- fastapi
- uvicorn
- pandas
- yfinance
- pydantic

Install all dependencies with:

```bash
pip install -r requirements.txt
```

## License

MIT License