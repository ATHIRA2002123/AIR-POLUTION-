import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.cluster import DBSCAN
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from scipy.spatial import distance

# STEP 1: Load Input Dataset
dataset = pd.read_csv("C:\\Users\Lenovo\Downloads\\archive\city_hour.csv")
print("=========================================")
print("Air Quality Prediction Indian Dataset")
print("=========================================")
print(dataset.head())

# STEP 2: Handle Missing Data (Impute missing values for numeric columns)
numeric_cols = dataset.select_dtypes(include=[np.number]).columns
imputer = SimpleImputer(strategy='mean')
dataset[numeric_cols] = imputer.fit_transform(dataset[numeric_cols])

# Convert categorical to numerical data using Label Encoding
label_encoder = preprocessing.LabelEncoder()
categorical_cols = ['City', 'AQI_Bucket']
dataset[categorical_cols] = dataset[categorical_cols].apply(label_encoder.fit_transform)

print("\n=========================================")
print("Dataset after categorical to numerical conversion")
print("=========================================")
print(dataset.head())

# Drop unnecessary columns (assuming column index 1 is unnecessary)
dataset.drop(dataset.columns[1], axis=1, inplace=True)

# Prepare data (features and labels)
X = dataset.iloc[:, :-1]  # Features
Y = dataset.iloc[:, -1].values  # Target variable (AQI_Bucket)

# STEP 3: Split dataset into training (70%) and testing (30%)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, shuffle=False)

# STEP 4: Predict Air Quality using DBSCAN with Linear Regression
# Perform DBSCAN clustering on training data
db = DBSCAN(eps=0.3, min_samples=10).fit(X_train)
labels = db.labels_

# Get the number of clusters and noise
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print(f"Estimated number of clusters: {n_clusters_}")
print(f"Estimated number of noise points: {n_noise_}")

# Plot DBSCAN clusters
plt.figure(figsize=(10, 6))
plt.scatter(X_train.iloc[:, 0], X_train.iloc[:, 1], c=labels, cmap='viridis', marker='o')
plt.title("DBSCAN Clusters on Training Data")
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.colorbar(label='Cluster Label')
plt.show()

# Perform Linear Regression on DBSCAN clustered data
DBSCANLR = LinearRegression()
DBSCANLR.fit(X_train, Y_train)
Y_pred = DBSCANLR.predict(X_test)
Y_pred = np.round(Y_pred).astype(int)  # Ensure integer class labels

# Print predicted values
print("\n=========================================")
print("DBSCAN with Linear Regression - Predicted Class Label Values for Testing Dataset")
print("=========================================")
print(Y_pred)

# STEP 5: Plot Actual vs Predicted values (Linear Regression Results)
plt.figure(figsize=(8, 5))
plt.scatter(Y_test, Y_pred, color='blue')
plt.plot([min(Y_test), max(Y_test)], [min(Y_test), max(Y_test)], color='red', linestyle='--')  # Ideal line where actual = predicted
plt.title("Actual vs Predicted Values")
plt.xlabel('Actual AQI_Bucket')
plt.ylabel('Predicted AQI_Bucket')
plt.show()

# STEP 6: Calculate accuracy using cosine similarity
DBSCANLRAccuracy = (1 - distance.cosine(Y_test, Y_pred)) * 100

print("\nGood --> 0\nModerate --> 1\nPoor --> 2\nSatisfactory --> 3\nSevere --> 4\nVery Poor --> 5\n")
print(f"DBSCAN with Linear Regression Accuracy: {DBSCANLRAccuracy:.2f} %")
print("=========================================")

# STEP 7: Visualize the accuracy with a bar chart
accuracy_data = {'Model': ['DBSCAN with LR'], 'Accuracy (%)': [DBSCANLRAccuracy]}
accuracy_df = pd.DataFrame(accuracy_data)

plt.figure(figsize=(6, 4))
sns.barplot(x='Model', y='Accuracy (%)', data=accuracy_df, hue='Model', legend=False)
plt.title('Model Accuracy')
plt.ylabel('Accuracy (%)')
plt.show()

# STEP 8: Residual Plot
residuals = Y_test - Y_pred
plt.figure(figsize=(8, 5))
plt.scatter(Y_pred, residuals, color='blue')
plt.axhline(0, color='red', linestyle='--')  # Zero residual line
plt.title('Residual Plot')
plt.xlabel('Predicted AQI_Bucket')
plt.ylabel('Residuals')
plt.show()

# STEP 9: Error Distribution Plot (Histogram of Residuals)
plt.figure(figsize=(8, 5))
sns.histplot(residuals, bins=20, kde=True, color='blue')
plt.title('Error Distribution (Residuals)')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.show()
