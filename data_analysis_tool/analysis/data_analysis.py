# Import necessary libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn
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

#create a countplot for gender

data['Gender'] = data['Gender'].where(data['Gender'].isin(['Male', 'Female']), 'Unknown')
df = pd.DataFrame(data)

X = data.drop(columns=['Billing Amount'])
y = data['Billing Amount']

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

print("Training set shape:", X_train.shape, y_train.shape)
print("Testing set shape:", X_test.shape, y_test.shape)
print("Features shape:", X.shape)
print("Target shape:", y.shape)



# Plot
# Create the countplot
ax = sns.countplot(data=data, x='Gender')

# Add title and labels
plt.title("Gender Distribution")
plt.xlabel('Gender')
plt.ylabel('Count')

# Add gridlines to show intercepts clearly
ax.yaxis.grid(True, linestyle='--', alpha=0.5)

# Add value labels on top of each bar
for p in ax.patches:
    height = p.get_height()
    ax.annotate(
        f'{height:,}',                      # formatted number
        (p.get_x() + p.get_width() / 2, height),
        ha='center', va='bottom',
        fontsize=12, fontweight='bold')
plt.show()



# Create a bar plot for the top 5 medical conditions
data["Medical Condition"].value_counts().head(5).plot(kind='bar')
plt.title("Top 5 Medical Conditions")
plt.tight_layout()
plt.xlabel('Medical Condition') 
plt.ylabel('Count')
plt.show()


#create a bar plot for the lenght of stay distribution
data['Date of Admission'] = pd.to_datetime(data['Date of Admission']) 
data['Discharge Date'] = pd.to_datetime(data['Discharge Date'])
data['Length of Stay'] = (data['Discharge Date'] - data['Date of Admission']).dt.days

sns.countplot(x='Length of Stay', data=data)
plt.title("Length of Stay distribution")
plt.xlabel('Length of Stay')
plt.ylabel('count')
plt.show()


#medical history distribution by blood type
data['Medical Condition'] = data['Medical Condition'].fillna('Unknown')
data['Blood Type'] = data['Blood Type'].fillna('Unknown')

sns.countplot(x='Medical Condition', hue='Blood Type', data=data)
plt.title("Medical history distribution by blood type")
plt.xlabel('Medical Condition')
plt.ylabel('count')
plt.show()



class DataAnalysis:
    def __init__(self, df):
        self.df = df

    def analyze_data(self):
        # Display dataset information
        print("FIRST 5 ROWS")
        print(self.df.head())

        print("LAST 5 ROWS")
        print(self.df.tail())

        print("DATA INFO")
        print(self.df.info())

        print("STATISTICAL SUMMARY")
        print(self.df.describe())

        # Check for null values
        print("NULL VALUES")
        print(self.df.isnull().sum())

        # Check duplicates
        print("\nDUPLICATES")
        print(self.df.duplicated().sum())

    def perform_analysis(self):
        self.analyze_data()

    def visualize_data(self):
            # Create a countplot for gender
            self.gender()
            def gender(self):
                self.df['Gender'] = self.df['Gender'].where(self.df['Gender'].isin(['Male', 'Female']), 'Unknown')
                df = pd.DataFrame(self.df)
                # Plot
                # Create the countplot
                ax = sns.countplot(data=df, x='Gender')

                plt.title("Gender Distribution")
                plt.xlabel('Gender')
                plt.ylabel('Count')

                # Add gridlines to show intercepts clearly
                ax.yaxis.grid(True, linestyle='--', alpha=0.5)

                # Add value labels on top of each bar
                for p in ax.patches:
                    height = p.get_height()
                ax.annotate(
                    f'{height:,}',                      # formatted number
                    (p.get_x() + p.get_width() / 2, height),
                    ha='center', va='bottom',
                    fontsize=12, fontweight='bold')
                plt.show()

            def medical_condition(self):
                # Create a bar plot for the top 5 medical conditions
                self.df["Medical Condition"].value_counts().head(5).plot(kind='bar')
                plt.title("Top 5 Medical Conditions")
                plt.tight_layout()
                plt.xlabel('Medical Condition') 
                plt.ylabel('Count')
                plt.show()

            def length_of_stay(self):
                # Create a bar plot for the length of stay distribution
                self.df['Date of Admission'] = pd.to_datetime(self.df['Date of Admission']) 
                self.df['Discharge Date'] = pd.to_datetime(self.df['Discharge Date'])
                self.df['Length of Stay'] = (self.df['Discharge Date'] - self.df['Date of Admission']).dt.days

                sns.countplot(x='Length of Stay', data=self.df)
                plt.title("Length of Stay distribution")
                plt.xlabel('Length of Stay')
                plt.ylabel('count')
                plt.show()

            def medical_history_blood_type(self):
                # Create a countplot for medical history distribution by blood type
                self.df['Medical Condition'] = self.df['Medical Condition'].fillna('Unknown')
                self.df['Blood Type'] = self.df['Blood Type'].fillna('Unknown')

                sns.countplot(x='Medical Condition', hue='Blood Type', data=self.df)
                plt.title("Medical history distribution by blood type")
                plt.xlabel('Medical Condition')
                plt.ylabel('count')
                plt.show()

        
            


















































































""" 




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
 """