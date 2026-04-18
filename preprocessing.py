import pandas as pd
import numpy as np
import os

df = pd.read_csv('C:\\DMW PROJECT\\data\\raw\\all_stocks_raw.csv')
print("Shape of Data:", df.shape)
#Missing values per column

print("\nMissing Values per column")
print(df.isnull().sum())

#Fixing the Date Column Data Type

print("\n Data types before fix:")
print(df.dtypes)

df['Date'] = pd.to_datetime(df['Date'])

print("\n Data Types after fix")
print(df.dtypes)

df = df.sort_values(['Ticker', 'Date'])

df = df.reset_index(drop = True)

# Feature 1 - Daily Return
df['Daily_Return'] = (df['Close'] - df['Open'] / df['Open'])

# Feature 2- 7- Day Moving Average
df['MA_7'] = df.groupby('Ticker')['Close'].transform(
    lambda x: x.rolling(window = 7).mean()

)
df['MA_21'] = df.groupby('Ticker')['Close'].transform(
    lambda x: x.rolling(window = 21).mean()

)


#Feature 4 - Volatility (7-day)

df['Volatility'] = df.groupby('Ticker')['Close'].transform(
    lambda x: x.rolling(window = 7).std()

)

# Feature 5: Target Column (What we Want to Predict)

df['Target'] = df.groupby('Ticker')['Close'].transform(
    lambda x: (x.shift(-1)>x).astype(int)
)
print("\n Missing Values after Feature Engineering:")
print(df.isnull().sum())

df = df.dropna()

print(f"\n Rows after dropping NAN : {len(df)}")

# Save Cleaned Data

os.makedirs('data/processed', exist_ok = True)
df.to_csv('C:\\DMW PROJECT\\data\\raw\\all_stocks_raw.csv', index = False)
print("\n PreProcessing Complete, Final Shape:" ,df.shape)
print("\n Sample of Processed Data")
print(df.head(10))
print("\n Column List:")
print(df.columns.tolist())
