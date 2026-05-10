# istalling necessary libraries
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('data_analysis_tool/data/healthcare_dataset.csv')
# Displaying the first few rows of the dataset
print(data.head())
print(data.tail())
print(data.info())
print(data.describe())

# checking for null values
print(data.isnull().sum())

# checking for duplicates
print(data.duplicated().sum())

# visualization
print(data.head())
sns.relplot("x='Name', y='Age', z= 'gender', hue= 'Blood Type', med= 'Medical condition', x='Date of Admission', do= 'Doctor', ho= 'Hospital', z= 'Insurance', b= 'Billing Amount', r= 'Room Number', a= 'Admission', y='Discharge Date', me= 'Medication', t= 'Test Results', kind= 'swarm', data= data")
plt.show()

#modeling
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Assuming 'Billing Amount' is the target variable and the rest are features
X = data.drop('Billing Amount', axis=1)
y = data['Billing Amount']
x_train, x_test, y_train, y_test = train_test_split(x, y , test_size=0.2, random_state=22)
regressor = LinearRegression()
regressor.fit(x_train, y_train)
y_pred = regressor.predict(x_test)
print("Predicted Billing Amounts:", y_pred)

# For simplicity, let's convert categorical variables to dummy variables
data_encoded = pd.get_dummies(X, drop_first=True)
x = data_encoded.drop('Billing Amount', axis=1)
y = data_encoded['Billing Amount']
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=22)
regressor.fit(x_train, y_train)
y_pred = regressor.predict(x_test)
print("Predicted Billing Amounts after encoding:", y_pred)
