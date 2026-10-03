import pandas as pd




###################   EVALUATE MODEL CODE #########################
import mlflow
import mlflow.sklearn
from sklearn.metrics import brier_score_loss


data = pd.read_csv("hotel_bookings_cleaned.csv")

month_number = pd.to_datetime(
    data["arrival_date_month"], format="%B"
).dt.month

arrival_date = pd.to_datetime({
    "year": data["arrival_date_year"],
    "month": month_number,
    "day": data["arrival_date_day_of_month"]
})

test = arrival_date >= "2017-05-01"

features = [
    "lead_time",
    "stays_in_weekend_nights",
    "stays_in_week_nights",
    "num_adults",
    "num_children",
    "num_babies"
]

X_test = data.loc[test, features].fillna(0)
y_test = data.loc[test, "is_canceled"]

mlflow.set_tracking_uri("sqlite:///mlflow.db")
model = mlflow.sklearn.load_model("models:/HotelCancellation/1")

probabilities = model.predict_proba(X_test)[:, 1]
score = brier_score_loss(y_test, probabilities)

print("Test bookings:", len(y_test))
print("Version 1 test Brier score:", score)
train = arrival_date < "2017-01-01"
baseline_probability = data.loc[train, "is_canceled"].mean()

baseline_score = brier_score_loss(
    y_test,
    [baseline_probability] * len(y_test)
)

print("Test baseline Brier score:", baseline_score)