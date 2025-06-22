# Stock Portfolio Project

A full-stack web application for managing and visualizing your personal stock portfolio, supporting US and HK markets. The project consists of a Python FastAPI backend and a Node.js/Express frontend dashboard.

---

## Project Structure

```
.
├── README.md                   # This file
├── stock-portfolio/            # Frontend (Node.js/Express + static dashboard)
│   ├── .gitignore
│   ├── package.json
│   ├── README.md
│   ├── public/
│   │   └── index.html          # Main dashboard UI
│   └── src/
│       └── server.js           # Express server for static files
└── stock-portfolio-api/        # Backend (Python FastAPI)
    ├── .gitignore
    ├── main.py                  # FastAPI server
    ├── README.md
    ├── requirements.txt
    └── stocks.csv              # Portfolio data (edit this file)
```

---

## Quick Start

### 1. Backend: Stock Portfolio API

The backend is a FastAPI that reads your holdings from `stocks.csv` and fetches live company names and prices using Yahoo Finance.

**Setup:**

```bash
cd stock-portfolio-api
pip install -r requirements.txt
python app.py
```

- The API will be available at [http://localhost:8000/api/stocks](http://localhost:8000/api/stocks).
- Edit `stocks.csv` to update your holdings.

See [stock-portfolio-api/README.md](stock-portfolio-api/README.md) for more details.

---

### 2. Frontend: Stock Portfolio Dashboard

The frontend is a Node.js/Express app that serves a static dashboard UI.

**Setup:**

```bash
cd stock-portfolio
npm install
npm start
```

- The dashboard will be available at [http://localhost:3000](http://localhost:3000).
- The dashboard fetches data from the FastAPI (`/api/stocks`).

See [stock-portfolio/README.md](stock-portfolio/README.md) for more details.

---

## Features

- **Live Portfolio Data:** Fetches company names and prices from Yahoo Finance.
- **Interactive Dashboard:** Visualizes holdings, market value, cost, and P/L.
- **Market Filtering:** View all holdings or filter by US/HK market.
- **Sortable Table:** Detailed, sortable holdings table.
- **Charts:** Portfolio composition and market performance visualizations.
- **Easy Data Management:** Update your holdings in `stocks.csv`.

---

## API Endpoint

- **GET `/api/stocks`**  
  Returns a JSON array of your holdings with live company names and prices.

---

## Requirements

- Python 3.8+ (for backend)
- Node.js 14+ (for frontend)

---

## License

MIT License

---

## Credits

- [fastapi](https://github.com/fastapi/fastapi/)
- [yfinance](https://github.com/ranaroussi/yfinance)
- [Express](https://expressjs.com/)
- [Chart.js](https://www.chartjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)