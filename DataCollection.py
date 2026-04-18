import yfinance as yf
import pandas as pd
import os
stocks = [
    'RELIANCE.NS','TCS.NS','INFY.NS','HDFCBANK.NS','WIPRO.NS'
]
start_date = '2022-01-01'
end_date = '2024-12-31'
try:
    os.makedirs('data/raw')
except FileExistsError:
    pass
all_data = []
for ticker in stocks:
  print(f"Downloading{ticker}....")
  df = yf.download(ticker, start = start_date, end = end_date)
  if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

  df['Ticker'] = ticker
  df.reset_index(inplace = True)
  df = df[['Date','Ticker','Open','High','Low','Close', 'Volume']]
  
  df.to_csv(f'data/raw/{ticker}_raw.csv', index = False)
  print(f"Saved {len(df)} rows for {ticker}")
  all_data.append(df)

combined_df = pd.concat(all_data, ignore_index=True)
combined_df.to_csv('data/raw/all_stocks_raw.csv', index = False)
print(f"\n Done! Total rows collected {len(combined_df)}")
print(combined_df.head())
print(combined_df.info())