import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns
import os
os.makedirs('outputs', exist_ok = True)
# Load Processed Data
df = pd.read_csv('C:\\DMW PROJECT\\data\\processed\\all_stocks_processed.csv')
df['Date'] = pd.to_datetime(df['Date'])
print("Data Shape:", df.shape)
#Bulding Stock Behaviour Profile

stock_profiles = df.groupby('Ticker').agg(
    avg_return = ('Daily_Return', 'mean'),
    avg_volatility = ('Volatility', 'mean'),
    avg_volume = ('Volume', 'mean'),
    avg_ma7 = ('MA_7', 'mean'),
    avg_ma21 = ('MA_21', 'mean')
).reset_index()
print("\n Stock Profiles:")
print(stock_profiles)
#Feature Scaling
features = ['avg_return', 'avg_volatility', 'avg_volume', 'avg_ma7', 'avg_ma21']
x = stock_profiles[features]
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)
print("\n Scaled Features:")
print(pd.DataFrame(x_scaled, columns = features))
#Using Elbow Method to find optimal K

inertia = []
k_range = range(2,5)
for k in k_range:
    km = KMeans(n_clusters = k, random_state = 42, n_init  = 10)
    km.fit(x_scaled)
    inertia.append(km.inertia_)
plt.figure(figsize=(6,4))
plt.plot(k_range, inertia, 'bo-', linewidth = 2, markersize = 8)
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal K')
plt.xticks(k_range)
plt.tight_layout()
plt.savefig('outputs//elbow_method.png')
plt.show()
print("Elbow Plot Saved")
print("\n Inertia Values:", inertia)

#Training KMeans with K=3
km_final = KMeans(n_clusters = 3, random_state = 42, n_init = 10)
km_final.fit(x_scaled)
stock_profiles['Cluster'] = km_final.labels_
print("\n Stock Profiles with Cluster Assignments:")
print(stock_profiles[['Ticker', 'Cluster', 'avg_return', 'avg_volatility']])
#Evaluation using Silhouette Score
sil_score = silhouette_score(x_scaled, km_final.labels_)
print(f"\n Silhouette Score for K=3: {sil_score:.4f}")

#Visualizing Clusters
plt.figure(figsize=(8,6))
colors = ['#e74c3c','#2ecc71','#3498db']
cluster_names = {0: 'Cluster 0', 1: 'Cluster 1', 2: 'Cluster 2'}

for cluster_id in range(3):
    mask = stock_profiles['Cluster'] == cluster_id
    subset = stock_profiles[mask]
    plt.scatter(subset['avg_return'], subset['avg_volatility'],
        label = cluster_names[cluster_id],
        color = colors[cluster_id],
        s = 200,
        zorder = 5
    )
    for _, row in subset.iterrows():
        plt.annotate(
            row['Ticker'],
            (row['avg_return'], row['avg_volatility']),
            textcoords = "offset points",
            xytext=(8, 5),
            fontsize = 9,
        )
plt.xlabel('Average Daily Return')
plt.ylabel('Average Volatility')
plt.title('Stock Clusters based on Behavior Profiles')
plt.legend()
plt.tight_layout()
plt.savefig('outputs//stock_clusters.png')
plt.show()
print("Cluster Plot Saved")

#Interpreting Each Cluster

print("\n Cluster Summary:")
summary = stock_profiles.groupby('Cluster')[features].mean().reset_index()
print(summary)
