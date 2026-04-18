import pandas as pd
import sqlite3
import os
df = pd.read_csv('C:\\DMW PROJECT\\data\\processed\\all_stocks_processed.csv')
df['Date'] = pd.to_datetime(df['Date'])
print("Loaded processed data:", df.shape)

#Creating DIM_DATE

dim_date = pd.DataFrame()
dim_date['date'] = pd.to_datetime(df['Date'].unique())
dim_date['day']  = dim_date['date'].dt.day
dim_date['month'] = dim_date['date'].dt.month
dim_date['year'] = dim_date['date'].dt.year
dim_date['quarter'] = dim_date['date'].dt.quarter
dim_date['day_of_week'] = dim_date['date'].dt.day_name()
dim_date = dim_date.sort_values('date').reset_index(drop = True)
dim_date['date_id'] = dim_date.index + 1
print("\n DIM_DATE sample:")
print(dim_date.head())

#Creating DIM_STOCK
company_info = {
    'RELIANCE.NS':('Reliance Industries', 'Energy'),
    'TCS.NS': ('Tata Consultancy Services', 'Information Technology'),
    'INFY.NS':('Infosys','Information Technology'),
    'HDFCBANK.NS':('HDFC Bank', 'Banking'),
    'WIPRO.NS':('Wipro', 'Information Technology')

}

dim_stock = pd.DataFrame([
    {'Ticker': ticker, 'company_name':info[0], 'sector':info[1]}
    for ticker, info in company_info.items()

])

dim_stock['stock_id'] = dim_stock.index + 1
print("\n DIM_STOCK sample:")
print(dim_stock)

#Merge date_id and stock_id into the main dataframe
df = df.merge(
    dim_date[['date', 'date_id']],
    left_on = 'Date',
    right_on = 'date',
    how = 'left'
)
print("DIM_STOCK columns:", dim_stock.columns.tolist())

df = df.merge(
    dim_stock[['Ticker', 'stock_id']],
    left_on = 'Ticker',
    right_on = 'Ticker',
    how = 'left'
)
fact = df[[
    'date_id', 'stock_id',
    'Open','High','Low','Close','Volume',
    'Daily_Return', 'MA_7', 'MA_21', 'Volatility', 'Target'

]].copy()

fact.columns=[
    'date_id', 'stock_id',
    'open_price', 'high_price', 'low_price', 'close', 'volume',
    'daily_return', 'ma_7', 'ma_21', 'volatility', 'target'
]

fact['fact_id'] = fact.index + 1
print("\n FACT_STOCK_PRICES sample:")
print(fact.head())

#Save to The SQLite Database

os.makedirs('C:\\DMW PROJECT\\data\\warehouse', exist_ok = True)
conn = sqlite3.connect('C:\\DMW PROJECT\\data\\warehouse\\stock_data_warehouse.db')
dim_date.to_sql('DIM_DATE', conn, if_exists = 'replace', index = False)
dim_stock.to_sql('DIM_STOCK', conn, if_exists = 'replace', index = False)
fact.to_sql('FACT_STOCK_PRICES', conn, if_exists = 'replace', index = False)

print("\n Tables saved to Database: ")

query = """
SELECT s.ticker, s.sector, d.year, d.quarter,
AVG(f.close) as avg_close
FROM FACT_STOCK_PRICES f
JOIN DIM_STOCK s ON f.stock_id = s.stock_id
JOIN DIM_DATE d ON f.date_id = d.date_id
GROUP BY s.ticker, d.year, d.quarter
ORDER BY s.ticker, d.year, d.quarter

"""

result = pd.read_sql(query, conn)
print("\n Sample warehouse query - Avg Close per stock per quarter:")
print(result.head(12))

conn.close()
print("\n Warehouse COmplete!")
