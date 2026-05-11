# Import necessary libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load dataset
data = pd.read_csv('data_analysis_tool/data/healthcare_dataset.csv')

# Display dataset information
print("FIRST 5 ROWS")
print(data.head())

print("LAST 5 ROWS")
print(data.tail())

print("DATA INFO")
print(data.info())

print("STATISTICAL SUMMARY")
print(data.describe())

# Check for null values
print("NULL VALUES")
print(data.isnull().sum())

# Check duplicates
print("\nDUPLICATES")
print(data.duplicated().sum())

# DATA VISUALIZATION

# Scatterplot: Age vs Billing Amount
plt.figure(figsize=(10, 6))

sns.scatterplot(
    x='Age',
    y='Billing Amount',
    hue='Gender',
    data=data
)

plt.title('Age vs Billing Amount')
plt.xlabel('Age')
plt.ylabel('Billing Amount')
plt.show()

# DATA PREPROCESSING
# Convert categorical columns into dummy variables
data_encoded = pd.get_dummies(data, drop_first=True)

# Features and target
X = data_encoded.drop('Billing Amount', axis=1)
y = data_encoded['Billing Amount']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=22
)


# MODEL TRAINING

model = LinearRegression()

# Train model
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)


# Display predicted billing amounts
print("PREDICTED BILLING AMOUNTS")
print(y_pred)

# Metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("MODEL PERFORMANCE")
print("Mean Squared Error:", mse)
print("R2 Score:", r2)
