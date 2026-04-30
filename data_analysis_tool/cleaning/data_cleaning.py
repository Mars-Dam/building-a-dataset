import os
import pandas as pd
import datetime

print(os.getcwd())

df = pd.read_csv("data_analysis_tool/data/healthcare_dataset.csv")

# Display the first few rows of the dataset
print(df.head())

df['Name'] = df['Name'].str.capitalize()

print(df.head())

df['Date of Admission'] = pd.to_datetime(df['Date of Admission'], errors='coerce')

print(df.head())

df['Discharge Date'] = pd.to_datetime(df['Discharge Date'], errors='coerce')
print(df.head())