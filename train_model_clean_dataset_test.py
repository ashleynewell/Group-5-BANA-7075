import pandas as pd




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

    # Save the same model already trained and logged to MLflow
    import joblib

    joblib.dump(model, "hotel_cancellation_predictor.pkl")
    print("Random Forest model saved!")