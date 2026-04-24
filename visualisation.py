import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
os.makedirs('outputs', exist_ok = True)
df = pd.read_csv('C:\\DMW PROJECT\\data\\processed\\all_stocks_processed.csv')
df['Date'] = pd.to_datetime(df['Date'])
# Visualizing Stock Price Trends
fig, axes = plt.subplots(5, 1, figsize=(12, 15))

tickers = df['Ticker'].unique()
colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6']
for i, ticker in enumerate(tickers):
    stock_data = df[df['Ticker'] == ticker]

    axes[i].plot(stock_data['Date'], stock_data['Close'], color = colors[i], linewidth = 1.2, label = 'Close Price')
    axes[i].plot(stock_data['Date'], stock_data['MA_21'],
                 color = 'black', linewidth = 1, linestyle='--',
                 alpha = 0.7, label = 'MA 21')
    axes[i].set_title(f'{ticker} Closing Price With 21-Day MA')
    axes[i].set_ylabel('Price (INR)')
    axes[i].legend(loc = 'upper left', fontsize = 8)
    axes[i].grid(True, alpha = 0.3)
axes[-1].set_xlabel('Date')
plt.suptitle('NSE Stock Price Trends (2022-2024)', fontsize = 14, y=1.01)
plt.tight_layout()
plt.savefig('outputs//price_trends.png', dpi = 150, bbox_inches = 'tight')
plt.show()
print("Price Trends Plot Saved")

feature_cols = ['Close','Volume','Daily_Return','MA_7','MA_21','Volatility','Target']
corr_matrix = df[feature_cols] .corr()
plt.figure(figsize=(8, 6))

sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".2f",
    cmap='coolwarm',
    center=0,
    square=True,
    linewidths=0.5
)
plt.title('Feature Correlation Heatmap')
plt.tight_layout()
plt.savefig('outputs//correlation_heatmap.png', dpi = 150)
plt.show()
print("Correlation Heatmap Saved")

# Visualizing Daily Return Distribution
plt.figure(figsize=(10, 5))

for i,ticker in enumerate(tickers):
    stock_data = df[df['Ticker'] == ticker]
    plt.hist(stock_data['Daily_Return'], bins = 50, alpha = 0.5, color = colors[i], label = ticker)

plt.xlabel('Daily Return')
plt.ylabel('Frequency')
plt.title('Distribution of Daily Returns for NSE Stocks')
plt.legend()
plt.axvline(x=0, color = 'black', linewidth = 1.5, linestyle='--')
plt.tight_layout()
plt.savefig('outputs//returns_distribution.png', dpi = 150)
plt.show()
print(" Returns Distribution Plot Saved")
