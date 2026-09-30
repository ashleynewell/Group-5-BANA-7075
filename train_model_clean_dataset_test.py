###################   DATASET CLEANUP MODEL CODE  ##################
##IMPORT PANDAS
import pandas as pd

##READ IN THE DATASET
hotel_bookings = pd.read_csv('hotel_bookings.csv')

#first look at the dataset. uncomment to have dataset viewable below
#print(hotel_bookings)

##REMOVE OR RENAME COLUMNS
#print(hotel_bookings.columns)
#removed because of data leakage. reveals prediction key variable
#hotel_bookings.drop(columns=['is_canceled'],inplace=True)
hotel_bookings.drop(columns=['previous_cancellations'],inplace=True)
hotel_bookings.drop(columns=['reservation_status'],inplace=True)
hotel_bookings.rename({'adults':'num_adults','children':'num_children','babies':'num_babies'},axis=1,inplace=True)

#sets the number of columns visible when printing
pd.set_option('display.max_columns', 10)
# Optional: Prevents wrapping to a new line if the screen is narrow
pd.set_option('display.width',None)
#check using only 10 rows. uncomment to have dataset viewable below
#print(hotel_bookings.head(10))

##CHECKING FOR CELLS THAT CONTAIN NaNs
hotel_bookings.isnull().sum() * 100 / len(hotel_bookings)
#check to see percentage of NaNs values. uncomment to view below
#print(hotel_bookings.isnull().sum() * 100 / len(hotel_bookings))

#Since 'company' column has approximately 94% NaNs, it will be removed from the dataset
hotel_bookings.drop(columns=['company'],inplace=True)
#test to see if it was removed
#print(hotel_bookings.isnull().sum() * 100 / len(hotel_bookings))

#checking for unique values in 'agent' column to determine next steps
#print(hotel_bookings['agent'].unique())
#inserts '-1' for cells with NaNs in the 'agent' column
hotel_bookings.fillna({'agent': -1}, inplace=True)

#checking for Nans in 'num_children' and 'country' columns
#print(hotel_bookings[hotel_bookings['num_children'].isna()])
#print(hotel_bookings[hotel_bookings['country'].isna()])

#replacing Nans in 'country' column with a string "unknown"
hotel_bookings.fillna({'country': 'unknown'}, inplace=True)
#dropping rows with Nans in 'num_children' column
hotel_bookings = hotel_bookings.dropna(subset=['num_children'])

##CHECK COLUMN DATA TYPES
#initial data types. uncomment to view below
#(hotel_bookings.dtypes)
hotel_bookings = hotel_bookings.astype({'is_repeated_guest':'boolean','num_children':'int'})
#check to see change in data type. uncomment to view below
#print(hotel_bookings.dtypes)


##STRING CLEANING
#checks for any outliers in columns with strings. uncomment to view below
#print(hotel_bookings['hotel'].unique())
#print(hotel_bookings['market_segment'].unique())
#print(hotel_bookings['distribution_channel'].unique())
#print(hotel_bookings['deposit_type'].unique())
#print(hotel_bookings['reserved_room_type'].unique())
#print(hotel_bookings['assigned_room_type'].unique())
#print(hotel_bookings['customer_type'].unique())

##REMOVE DUPLICATES
#checks whether each row is a duplicated value or not
hotel_bookings.loc[hotel_bookings.duplicated(keep=False)]
#drops rows of data where all the columns are the same
hotel_bookings.drop_duplicates(keep="first", inplace = True)
#check. uncomment to view below
#print(hotel_bookings.loc[hotel_bookings.duplicated(keep=False)])


##BIN COLUMNS
# Grouped continuous numerical data (like lead_time) into categorical buckets
bins = [-1, 7, 30, 90, 365, float('inf')]
labels = ['Last Minute', 'Short-term', 'Medium-term', 'Long-term', 'Extended']
hotel_bookings['lead_time_binned'] = pd.cut(hotel_bookings['lead_time'], bins=bins, labels=labels)
# check the binned column. uncomment to view below
# print(hotel_bookings[['lead_time', 'lead_time_binned']].head(10))

##VERSIONING AND EXPORTING DATASET
# Exported the cleaned dataset to a new CSV file instead of overwriting the original
hotel_bookings.to_csv('hotel_bookings_cleaned.csv', index=False)

##GROUPING AND SPLITTING DATASET
# Using scikit-learn to split the data for modeling (Train vs Test vs Production)
from sklearn.model_selection import train_test_split

# Split into 70% training and 30% temporary holdout
train_df, temp_df = train_test_split(hotel_bookings, test_size=0.3, random_state=42)

# Split the 30% holdout evenly into testing and production datasets (15% each)
test_df, prod_df = train_test_split(temp_df, test_size=0.5, random_state=42)

# Save the individual split datasets as new CSV files
train_df.to_csv('hotel_bookings_train.csv', index=False)
test_df.to_csv('hotel_bookings_test.csv', index=False)
prod_df.to_csv('hotel_bookings_prod.csv', index=False)

##DVC VERSIONING SETUP (Run these commands in the PyCharm terminal)
# 1. install dvc: pip install dvc
# 2. initialize dvc in the project: dvc init
# 3. track the cleaned dataset: dvc add hotel_bookings_cleaned.csv
# 4. commit the dvc tracking file to git:
#    git add hotel_bookings_cleaned.csv.dvc .gitignore
#    git commit -m "Track cleaned hotel bookings dataset with DVC"



###################   TRAINING MODEL CODE #########################

import mlflow.sklearn

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import brier_score_loss

# Load the data
data = pd.read_csv("hotel_bookings_cleaned.csv")

print("Number of bookings:", len(data))
print(data["is_canceled"].value_counts())


# Separate the answer from the inputs
y = data["is_canceled"]

X = data.drop(columns=[
    "is_canceled",
    #"reservation_status",
    #"reservation_status_date"
])

print("Inputs:", X.shape)
print("Answers:", y.shape)


# Create arrival dates
month_number = pd.to_datetime(
    data["arrival_date_month"],
    format="%B"
).dt.month

arrival_date = pd.to_datetime({
    "year": data["arrival_date_year"],
    "month": month_number,
    "day": data["arrival_date_day_of_month"]
})

print("Earliest arrival:", arrival_date.min())
print("Latest arrival:", arrival_date.max())


# Split bookings by arrival date
train = arrival_date < "2017-01-01"
validation = (
    (arrival_date >= "2017-01-01")
    & (arrival_date < "2017-05-01")
)
test = arrival_date >= "2017-05-01"

print("Training:", train.sum())
print("Validation:", validation.sum())
print("Testing:", test.sum())


# Train a first Random Forest model
features = [
    "lead_time",
    "stays_in_weekend_nights",
    "stays_in_week_nights",
    "num_adults",
    "num_children",
    "num_babies"
]

X_train = X.loc[train, features].fillna(0)
X_validation = X.loc[validation, features].fillna(0)

model = RandomForestClassifier(
    n_estimators=50,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y.loc[train])

probabilities = model.predict_proba(X_validation)[:, 1]
model_score = brier_score_loss(y.loc[validation], probabilities)

print("Validation Brier score:", model_score)


# Compare with a simple baseline
baseline_probability = y.loc[train].mean()
baseline_predictions = [baseline_probability] * validation.sum()

baseline_score = brier_score_loss(
    y.loc[validation],
    baseline_predictions
)

print("Simple baseline Brier score:", baseline_score)


# Track the experiment and register the model
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("Hotel cancellation")

with mlflow.start_run(run_name="Random Forest first model"):
    mlflow.log_param("model", "Random Forest")
    mlflow.log_param("n_estimators", 50)
    mlflow.log_param("max_depth", 10)
    mlflow.log_metric("validation_brier", model_score)
    mlflow.log_metric("baseline_brier", baseline_score)

    mlflow.sklearn.log_model(
        sk_model=model,
        name="random_forest_model",
        registered_model_name="HotelCancellation",
        skops_trusted_types=["sklearn.tree._tree.Tree"]
    )

    print("MLflow run saved")