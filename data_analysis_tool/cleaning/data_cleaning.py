import os
import pandas as pd
import datetime

print(os.getcwd())

df = pd.read_csv("data_analysis_tool/data/healthcare_dataset.csv")

""" # Display the first few rows of the dataset
print(df.head())

df.info()
df.isnull().sum()
df.duplicated().sum()

df['Name'] = df['Name'].str.capitalize()
df['Date of Admission'] = pd.to_datetime(df['Date of Admission'], errors='coerce')
df['Discharge Date'] = pd.to_datetime(df['Discharge Date'], errors='coerce')

 """

class data_cleaning():
    def __init__(self, df):
        self.df = df

    def clean_data(self):
        self.df['Name'] = self.df['Name'].str.capitalize()
        self.df['Date of Admission'] = pd.to_datetime(self.df['Date of Admission'], errors='coerce')
        self.df['Discharge Date'] = pd.to_datetime(self.df['Discharge Date'], errors='coerce')
        return self.df
    
"""     def save_cleaned_data(self, cleaned_df):
        cleaned_df.to_csv("data_analysis_tool/data/cleaned_healthcare_dataset.csv", index=False)
        print("Cleaned data saved to: data_analysis_tool/data/cleaned_healthcare_dataset.csv")

cleaner = data_cleaning(df)
cleaned_df = cleaner.clean_data()
cleaner.save_cleaned_data(cleaned_df)

 """


