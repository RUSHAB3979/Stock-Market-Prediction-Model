import pandas as pd
import numpy as npp
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs('outputs', exist_ok = True)
# Load Processed Data
df = pd.read_csv('C:\\DMW PROJECT\\data\\processed\\all_stocks_processed.csv')
df['Date'] = pd.to_datetime(df['Date'])
print("Dates Shpae:" ,df.shape)
print("Target distribution")
print(df['Target'].value_counts())

#Defininf Features and Target
features = ['Volume','Daily_Return', 'MA_7', 'MA_21', 'Volatility']
x = df[features]
y = df['Target']

print("\n Features Shape:", x.shape)
print("Target Shape:", y.shape)

# Train Test Split
x_train, x_test, y_train, y_test = train_test_split(
    x,y,
    test_size = 0.2,
    random_state = 42,
    shuffle = False
)
print(f"\n  Training set: {len(x_train)}")
print(f" Test set: {len(x_test)}")
# Train Decision Tree Classifier
model = DecisionTreeClassifier(
    max_depth=5,
    random_state = 42,
    class_weight = 'balanced')
model.fit(x_train, y_train)

print("Model Trained")

y_pred = model.predict(x_test)

print("\n First 10 Predictions:", y_pred[:10])
print("Actual ", y_test.values[:10])
# Evaluation
accuracy = accuracy_score(y_test, y_pred)
print(f"\n Accuracy: {accuracy:.4f}({accuracy*100:.2f}%)")
print(classification_report(y_test, y_pred))
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6,4))
sns.heatmap(cm, annot = True, fmt = 'd', cmap = 'Blues',
            xticklabels=['Predicted DOWN', 'Predicted UP'],
            yticklabels=['Actual Down', 'Actual UP'])
plt.title('Decision Tree - Confusion Matrix')
plt.tight_layout()
plt.savefig('outputs//confusion_matrix.png')
plt.show()
print("Confusion Matrix Saved")

#Feature Importance
importance  = pd.DataFrame({
    'Feature': features,
    'Importance': model.feature_importances_

}).sort_values('Importance', ascending = False)

print("\n Feature Importances")
print(importance)

plt.figure(figsize=(8,5))
sns.barplot(data = importance, x = 'Importance', y = 'Feature', palette = 'viridis')
plt.title('Feature Importance  -   Decision Tree')
plt.tight_layout()
plt.savefig('outputs//feature_importance.png')
plt.show()
print("Feature Importance Plot Saved")
