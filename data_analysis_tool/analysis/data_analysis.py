# Import necessary libraries
import os
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
DATA_PATH = os.path.join(REPO_ROOT, 'data_analysis_tool', 'data', 'healthcare_dataset.csv')
OUTPUT_DIR = os.path.join(REPO_ROOT, 'data_analysis_tool', 'plots')
os.makedirs(OUTPUT_DIR, exist_ok=True)


data = pd.read_csv(DATA_PATH)


def prepare_feature_data(dataframe, columns_to_drop):
    feature_data = dataframe.drop(columns=columns_to_drop).copy()
    feature_data = feature_data.fillna({'Gender': 'Unknown'})

    for column in feature_data.select_dtypes(include=['object', 'string']).columns:
        feature_data[column] = feature_data[column].fillna('Unknown').astype(str)

    for column in feature_data.select_dtypes(exclude=['object', 'string']).columns:
        feature_data[column] = feature_data[column].fillna(0)

    return feature_data


def save_plot(figure, filename):
    figure.tight_layout()
    plot_path = os.path.join(OUTPUT_DIR, filename)
    figure.savefig(plot_path, dpi=300)
    plt.close(figure)
    print(f'Saved plot to {plot_path}')
    plt.show()


def plot_gender_distribution(dataframe):
    plt.figure(figsize=(6, 4))
    ax = sns.countplot(data=dataframe, x='Gender')
    plt.title('Gender Distribution')
    plt.xlabel('Gender')
    plt.ylabel('Count')
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)

    for patch in ax.patches:
        height = patch.get_height()
        ax.annotate(
            f'{height:,}',
            (patch.get_x() + patch.get_width() / 2, height),
            ha='center',
            va='bottom',
            fontsize=12,
            fontweight='bold',
        )

    save_plot(plt.gcf(), 'gender_distribution.png')


def plot_top_medical_conditions(dataframe):
    top_5 = dataframe['Medical Condition'].value_counts().head(5)
    plt.figure(figsize=(8, 4))
    ax = top_5.plot(kind='bar', color='skyblue', edgecolor='black')

    for container in ax.containers:
        ax.bar_label(container, fmt='%d', label_type='edge', padding=3)

    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: f'{int(x):,}'))
    plt.ylim(bottom=9000)
    plt.title('Top 5 Medical Conditions with Counts')
    plt.xlabel('Medical Condition')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')

    save_plot(plt.gcf(), 'top_medical_conditions.png')


def plot_length_of_stay(dataframe):
    working_df = dataframe.copy()
    working_df['Date of Admission'] = pd.to_datetime(working_df['Date of Admission'], errors='coerce')
    working_df['Discharge Date'] = pd.to_datetime(working_df['Discharge Date'], errors='coerce')
    working_df['Length of Stay'] = (working_df['Discharge Date'] - working_df['Date of Admission']).dt.days

    plt.figure(figsize=(8, 4))
    sns.countplot(x='Length of Stay', data=working_df)
    plt.title('Length of Stay Distribution')
    plt.xlabel('Length of Stay')
    plt.ylabel('Count')

    save_plot(plt.gcf(), 'length_of_stay_distribution.png')


def plot_medical_history_by_blood_type(dataframe):
    working_df = dataframe.copy()
    working_df['Medical Condition'] = working_df['Medical Condition'].fillna('Unknown')
    working_df['Blood Type'] = working_df['Blood Type'].fillna('Unknown')

    plt.figure(figsize=(10, 4))
    sns.countplot(x='Medical Condition', hue='Blood Type', data=working_df)
    plt.title('Medical History Distribution by Blood Type')
    plt.xlabel('Medical Condition')
    plt.ylabel('Count')

    save_plot(plt.gcf(), 'medical_history_by_blood_type.png')


print('FIRST 5 ROWS')
print(data.head())

print('LAST 5 ROWS')
print(data.tail())

print('DATA INFO')
print(data.info())

print('STATISTICAL SUMMARY')
print(data.describe())

print('NULL VALUES')
print(data.isnull().sum())

print('\nDUPLICATES')
print(data.duplicated().sum())

# Visualization section
plot_gender_distribution(data)
plot_top_medical_conditions(data)
plot_length_of_stay(data)
plot_medical_history_by_blood_type(data)


def build_confusion_matrices(dataframe, output_folder):
    working_df = dataframe.copy()
    working_df['Gender'] = working_df['Gender'].fillna('Unknown')
    working_df['Gender'] = working_df['Gender'].where(working_df['Gender'].isin(['Male', 'Female']), 'Unknown')

    median_amount = working_df['Billing Amount'].median()
    working_df['Billing Category'] = working_df['Billing Amount'].ge(median_amount).astype(int).map({0: 'Low', 1: 'High'})
    working_df['Gender-Based Prediction'] = (
        working_df['Gender'].fillna('Unknown').str.strip().str.title().map({'Male': 'High', 'Female': 'Low', 'Unknown': 'Low'})
    )

    cm = confusion_matrix(
        working_df['Billing Category'].astype(str),
        working_df['Gender-Based Prediction'].astype(str),
        labels=['Low', 'High'],
    )

    plt.figure(figsize=(6, 4))
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Blues',
        xticklabels=['Predicted Low', 'Predicted High'],
        yticklabels=['Actual Low', 'Actual High'],
    )
    plt.title('Confusion Matrix: Gender vs Billing Amount')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    save_plot(plt.gcf(), 'gender_billing_confusion_matrix.png')

    for target_col in ['Medical Condition', 'Medication']:
        feature_data = prepare_feature_data(working_df, ['Billing Amount', target_col, 'Name'])
        target_data = working_df[target_col].fillna('Unknown').astype(str)

        X_train, X_test, y_train, y_test = train_test_split(
            feature_data,
            target_data,
            test_size=0.2,
            random_state=42,
            stratify=target_data,
        )

        categorical_features = feature_data.select_dtypes(include=['object', 'string']).columns
        numeric_features = feature_data.select_dtypes(exclude=['object', 'string']).columns

        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
                ('num', 'passthrough', numeric_features),
            ]
        )

        model = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', DecisionTreeClassifier(random_state=42)),
        ])

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        labels = sorted(set(y_test.astype(str)).union(set(y_pred.astype(str))))
        cm = confusion_matrix(y_test, y_pred, labels=labels)

        plt.figure(figsize=(max(6, len(labels) * 1.4), max(4, len(labels) * 1.2)))
        sns.heatmap(
            cm,
            annot=True,
            fmt='d',
            cmap='Blues',
            xticklabels=labels,
            yticklabels=labels,
        )
        plt.title(f'Confusion Matrix: {target_col}')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        save_plot(plt.gcf(), f'{target_col.lower().replace(" ", "_")}_confusion_matrix.png')

    for target_col in ['Date of Admission', 'Discharge Date']:
        feature_data = prepare_feature_data(working_df, [target_col, 'Billing Amount', 'Name'])
        target_data = pd.to_datetime(working_df[target_col], errors='coerce').dt.to_period('M').astype(str)

        X_train, X_test, y_train, y_test = train_test_split(
            feature_data,
            target_data,
            test_size=0.2,
            random_state=42,
        )

        categorical_features = feature_data.select_dtypes(include=['object', 'string']).columns
        numeric_features = feature_data.select_dtypes(exclude=['object', 'string']).columns

        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
                ('num', 'passthrough', numeric_features),
            ]
        )

        model = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', DecisionTreeClassifier(random_state=42)),
        ])

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        labels = sorted(set(y_test.astype(str)).union(set(y_pred.astype(str))))
        cm = confusion_matrix(y_test, y_pred, labels=labels)

        plt.figure(figsize=(max(6, len(labels) * 1.4), max(4, len(labels) * 1.2)))
        sns.heatmap(
            cm,
            annot=True,
            fmt='d',
            cmap='Blues',
            xticklabels=labels,
            yticklabels=labels,
        )
        plt.title(f'Confusion Matrix: {target_col} (Month-Year)')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        save_plot(plt.gcf(), f'{target_col.lower().replace(" ", "_")}_confusion_matrix.png')


# Machine learning analysis runs after the visualizations above.
build_confusion_matrices(data, OUTPUT_DIR)
