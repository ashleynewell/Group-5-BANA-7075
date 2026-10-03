# Group-5-BANA-7075

# 🏨 Hotel Cancellation Prediction System

The ML system predicts the probability that a hotel reservation will be canceled and identifies booking characteristics associated with cancellation risk. Hotels can use these predictions to support occupancy forecasting and estimate potential revenue at risk.

This information can help hotels better manage cancellations, plan for demand, and reduce potential revenue loss.

## Table of Contents

- 📁 Data Sources
- 🏗️ Model Architecture
- 📈 Performance Metrics
- 🧪 Testing & Validation
- ✨ Features
- 💡 Use Cases
- ⚙️ Installation
- 📖 Example
- 🚀 Usage
- 🤝 Contributing
- 📚 Documentation
- ⏳ History
- 📄 License

## 📁 Data Sources

This project uses the Hotel Booking Demand dataset.

The original dataset is stored as:

`hotel_bookings.csv`

The data preparation process creates cleaned and split versions of the data for model development and evaluation.

## 🏗️ Model Architecture

```text
├── hotel_bookings.csv
├── hotel_bookings_cleaned.csv
├── hotel_bookings_train.csv
├── hotel_bookings_test.csv
├── hotel_bookings_prod.csv
│
├── prepare_data.py
├── train_model_clean_dataset_test.py
├── compare_model_clean_dataset_test.py
├── evaluate_model_clean_dataset_test.py
│
├── Prediction.py
├── Dashboard.py
│
└── hotel_cancellation_predictor.pkl
```

The primary prediction model is a Random Forest classifier. Logistic Regression is also used as a comparison model.

MLflow is used for experiment tracking and model versioning.

## 📈 Performance Metrics

The project evaluates model performance using the **Brier Score**, which measures the accuracy of probability predictions.

A lower Brier Score represents better probability predictions.

The Random Forest model is also compared against:

- A simple cancellation-rate baseline
- Logistic Regression

### Final Test Results

- **Test bookings:** 17,735
- **Version 1 Random Forest test Brier Score:** 0.2188
- **Test baseline Brier Score:** 0.2360

Because a lower Brier Score is better, the registered Version 1 model performed better than the simple baseline on the test data.

## 🧪 Testing & Validation

The project uses time-based validation so that later hotel reservations are used to evaluate models trained on earlier reservations.

The modeling workflow separates bookings into:

- Training data
- Validation data
- Testing data

The final model is evaluated on the test period after model development and comparison.

## ✨ Features

- Hotel reservation cancellation probability prediction
- Automated data preparation
- Random Forest model training
- Logistic Regression comparison
- MLflow experiment tracking
- MLflow model registration
- Model evaluation using Brier Score
- Local saved prediction model
- CSV-based reservation input
- Improved dashboard user interface with upload and clear buttons
- Sorting and filtering capabilities
- Easy-to-read summary table with customizable booking information
- Quantitative summary of total bookings and high- and low-risk counts
- Conditional metric coloring for cancellation risk
- Current high/low risk threshold set at 50%, with the ability to adjust the threshold
- DVC-ready dataset versioning workflow

## 💡 Use Cases

**1. Predicting Cancellation Risk for Individual Reservations**

> Hotels can input upcoming reservations and receive a cancellation probability score for each booking. This can help staff identify reservations with higher cancellation risk.

**2. Monthly and Seasonal Occupancy Forecasting**

> By analyzing cancellation probabilities, hotels can improve occupancy forecasts and support staffing and resource planning.

**3. Revenue-at-Risk Estimation**

> Cancellation probabilities can eventually be combined with reservation values to estimate potential revenue loss and support pricing or overbooking decisions.

## ⚙️ Installation

Python 3 is required.

Install the primary Python packages with:

```powershell
pip install pandas scikit-learn mlflow joblib dvc
```

Tkinter is included with most standard Python installations.

Place `hotel_bookings.csv` in the same folder as the Python scripts.

## 📖 Example

The dashboard accepts a CSV containing reservation information.

The prediction model currently requires these columns:

```text
lead_time
stays_in_weekend_nights
stays_in_week_nights
num_adults
num_children
num_babies
```

The application returns the predicted probability that the reservation will be canceled.

## 🚀 Usage

### Prepare the data

Run:

```powershell
py .\prepare_data.py
```

This creates `hotel_bookings_cleaned.csv` and the train, test, and production datasets.

### Train the Random Forest model

Run:

```powershell
py .\train_model_clean_dataset_test.py
```

This trains the Random Forest, records the experiment in MLflow, registers the model, and saves:

```text
hotel_cancellation_predictor.pkl
```

### Compare models

Run:

```powershell
py .\compare_model_clean_dataset_test.py
```

This trains the Logistic Regression comparison model and records the results in MLflow.

### Evaluate the model

Run:

```powershell
py .\evaluate_model_clean_dataset_test.py
```

The evaluation script currently loads version 1 of `HotelCancellation` from the local MLflow database.

### Run the dashboard

After the prediction model has been created, run:

```powershell
py .\Dashboard.py
```

Select a properly formatted reservation CSV file when prompted.

The dashboard displays cancellation-risk results in a summary table and supports sorting, filtering, and customizable views. It also provides total booking counts and high- and low-risk counts. Risk coloring is currently based on a 50% cancellation-probability threshold, which can be changed depending on the desired risk tolerance.

## 🤝 Contributing

Project changes are managed through GitHub.

The team uses Issues, branches, Pull Requests, reviews, and merges to document changes and collaborate on project development.

## 📚 Documentation

Important project files include:

- `prepare_data.py` — prepares and exports the cleaned dataset
- `train_model_clean_dataset_test.py` — trains and logs the Random Forest model
- `compare_model_clean_dataset_test.py` — compares the Logistic Regression model
- `evaluate_model_clean_dataset_test.py` — evaluates the registered model
- `Prediction.py` — generates cancellation probabilities
- `Dashboard.py` — provides the user-facing prediction interface

## ⏳ History

Updated October 3, 2026.

Recent development included reducing repeated data-cleaning and model-training steps, improving runtime, adding the prediction application, and continuing development of the dashboard interface.

## 📄 License

This project was developed for academic coursework and is not licensed for external commercial use.
