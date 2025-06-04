import pandas as pd

# Data from your table
data = {
    'market': ['US', 'US', 'HK', 'HK', 'US'],
    'symbol': ['AAPL', 'MSFT', '0005.HK', '0700.HK', 'GOOG'],
    # 'company': ['Apple Inc.', 'Microsoft Corp.', 'HSBC Holdings plc', 'Tencent Holdings Ltd.', 'Alphabet Inc.'],
    'currency': ['USD', 'USD', 'HKD', 'HKD', 'USD'],
    'shares': [100, 50, 500, 200, 20],
    'avgCost': [170.50, 400.00, 62.80, 300.00, 150.00],
    # 'currentPrice': [175.20, 405.50, 63.50, 298.00, 152.00]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('stocks-2.csv', index=False)

print("stocks.csv created successfully!")