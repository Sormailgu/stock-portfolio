const express = require('express');
const xlsx = require('xlsx');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, '../public')));

// Endpoint to get stock data from the Excel file
app.get('/api/stocks', (req, res) => {
    const filePath = path.join(__dirname, '../public/stocks.xlsx');
    const workbook = xlsx.readFile(filePath);
    const sheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[sheetName];
    const stockData = xlsx.utils.sheet_to_json(worksheet);

    res.json(stockData);
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});