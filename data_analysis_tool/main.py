import pandas as pd
from auth.auth import Auth
from analysis.data_analysis import DataAnalysis
from utils.navigation import navigation_menu
from cleaning.data_cleaning import data_cleaning


def main():
    # Authenticate user
    auth = Auth()
    user = auth.login()
    if user is None:
        print("Authentication failed. Exiting the program.")
        return


    # Load and clean data
    df = pd.read_csv("data_analysis_tool/data/healthcare_dataset.csv")
    cleaner = data_cleaning(df)
    cleaned_df = cleaner.clean_data()

    # Perform data analysis
    analysis = DataAnalysis(cleaned_df)
    analysis.perform_analysis()

    navigation_menu()
    


if __name__ == "__main__":
    main()