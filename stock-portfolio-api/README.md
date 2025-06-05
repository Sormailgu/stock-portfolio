# Stock Portfolio API

This is a Flask-based API that provides stock portfolio data, including company names and current prices, by reading from a CSV file and fetching live data using Yahoo Finance.

## Features

- Reads stock holdings from `stocks.csv`
- Fetches company names and current prices using [yfinance](https://github.com/ranaroussi/yfinance)
- Caches results for efficiency
- CORS enabled for frontend integration

## Project Structure

```
stock-portfolio-api/
├── app.py           # Main Flask API server
├── requirements.txt # Python dependencies
├── stocks.csv       # Portfolio data (edit this file to update holdings)
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
   python app.py
   ```

   The API will be available at [http://localhost:5001/api/stocks](http://localhost:5001/api/stocks).

## API Endpoint

### `GET /api/stocks`

Returns a JSON array of your stock holdings with live company names and prices.

**Example response:**

```json
[
  {
    "market": "US",
    "symbol": "AAPL",
    "company": "Apple Inc.",
    "currency": "USD",
    "shares": 10,
    "avgCost": 150,
    "currentPrice": 175.2
  }
]
```

## Notes

- The API fetches live data from Yahoo Finance. If a symbol is invalid or data is unavailable, an error will be returned.
- The server uses an in-memory cache for efficiency. Restarting the server will clear the cache.

## Dependencies

- Flask
- flask-cors
- pandas
- yfinance
- openpyxl

Install all dependencies with:

```bash
pip install -r requirements.txt
```

## License

MIT License