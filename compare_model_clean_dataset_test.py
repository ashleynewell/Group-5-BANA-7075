import pandas as pd



###################   COMPARE MODEL CODE #########################
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss


data = pd.read_csv("hotel_bookings_cleaned.csv")
y = data["is_canceled"]

month_number = pd.to_datetime(
    data["arrival_date_month"], format="%B"
).dt.month

arrival_date = pd.to_datetime({
    "year": data["arrival_date_year"],
    "month": month_number,
    "day": data["arrival_date_day_of_month"]
})

train = arrival_date < "2017-01-01"
validation = (
    (arrival_date >= "2017-01-01")
    & (arrival_date < "2017-05-01")
)

features = [
    "lead_time",
    "stays_in_weekend_nights",
    "stays_in_week_nights",
    "num_adults",
    "num_children",
    "num_babies"
]

X_train = data.loc[train, features].fillna(0)
X_validation = data.loc[validation, features].fillna(0)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y.loc[train])

probabilities = model.predict_proba(X_validation)[:, 1]
score = brier_score_loss(y.loc[validation], probabilities)

print("Logistic Regression Brier score:", score)


# Record the comparison in the same MLflow experiment
import mlflow
import mlflow.sklearn

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("Hotel cancellation")

with mlflow.start_run(run_name="Logistic Regression comparison"):
    mlflow.log_param("model", "Logistic Regression")
    mlflow.log_param("max_iter", 1000)
    mlflow.log_metric("validation_brier", score)
    mlflow.sklearn.log_model(
        sk_model=model,
        name="logistic_regression_model"
    )

print("Comparison run saved")