import pandas as pd
import joblib


# Load the trained Random Forest
model = joblib.load("hotel_cancellation_predictor.pkl")


# These must match the features used during training
FEATURES = [
    "lead_time",
    "stays_in_weekend_nights",
    "stays_in_week_nights",
    "num_adults",
    "num_children",
    "num_babies"
]


def make_prediction(csv_file):

    # Read the customer's CSV
    data = pd.read_csv(csv_file)

    # Check that required columns exist
    missing_columns = [
        column for column in FEATURES
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Select only the columns the Random Forest uses
    X = data[FEATURES].fillna(0)

    # Get cancellation probability
    probabilities = model.predict_proba(X)[:, 1]

    return probabilities