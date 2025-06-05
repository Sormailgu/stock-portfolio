# Stock Portfolio Dashboard

## Overview
The Stock Portfolio Dashboard is an interactive web application that allows users to manage and visualize their stock holdings from the US and HK markets. The dashboard provides key performance indicators (KPIs), charts for portfolio composition and market performance, and a detailed sortable table of holdings.

## Project Structure
```
stock-portfolio
├── public
│   └── index.html         # HTML structure for the dashboard
├── src
│   └── server.js          # Server-side script to serve API and static files
├── package.json           # npm configuration file with dependencies
└── README.md              # Documentation for the project
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd stock-portfolio
   ```

2. **Install Dependencies**
   Make sure you have Node.js installed. Then run:
   ```bash
   npm install
   ```

3. **Run the Server**
   Start the server using:
   ```bash
   node src/server.js
   ```
   The server will be running on `http://localhost:3000`.

4. **Access the Dashboard**
   Open your web browser and navigate to `http://localhost:3000` to view the Stock Portfolio Dashboard.

## Usage
- Use the filter buttons to view stocks from specific markets (All, US, HK).
- The dashboard displays key metrics such as Total Market Value, Total Cost, and Unrealized P/L.
- Visualizations include a Doughnut chart for portfolio composition and a Bar chart for market performance.
- The detailed holdings table allows sorting by various columns.

## API Usage

All stock data is now fetched from an API endpoint:

- **GET /api/stocks**
  - Returns: JSON array of stock holdings.
  - Example response:
    ```json
    [
      {
        "Market": "US",
        "Symbol": "AAPL",
        "Company": "Apple Inc.",
        "Currency": "USD",
        "Shares": 10,
        "AvgCost": 150,
        "CurrentPrice": 175
      }
    ]
    ```
  - You can call this endpoint from your frontend code or with tools like `curl`:
    ```bash
    curl http://localhost:5001/api/stocks
    ```

## Dependencies
- **Express**: Web framework for Node.js.
- **Any other dependencies used by your API**

## License
This project is licensed under the MIT License. See the LICENSE file for details.