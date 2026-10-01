# Group-5-BANA-7075
# :hotel: Hotel Cancellation Prediction System
The ML system will predict the probability that a hotel reservation will be canceled and identify the booking characteristics associated with higher cancellation risk. Hotels can aggregate these predictions by month or season to support occupancy forecasting and combine predicted cancellation probabilities with reservation values to estimate potential revenue at risk. This information can help hotels better manage cancellations, plan for demand, and reduce potential revenue loss.

## Table of Contents
- :file_folder: Data Sources
- :building_construction: Model Architecture
- :chart_with_upwards_trend: Performance Metrics
- :test_tube: Testing & Validation
- :sparkles: Features
- :bulb: Use Cases
- :gear: Installation
- :book: Example
- :rocket: Usage
- :handshake: Contributing
- :books: Documentation
- :hourglass_flowing_sand: History
- :page_facing_up: License


## :file_folder: Data Sources

## :building_construction: Model Architecture


├── hotel_bookings.csv

├── hotel_bookings_cleaned.csv

├── hotel_bookings_train.csv

├── hotel_bookings_test.csv

├── hotel_bookings_prod.csv

│

├── prediction.py

├── dashboard.py

│

└── random_forest_model.pkl


## :chart_with_upwards_trend: Performance Metrics

## :test_tube: Testing & Validation


## :sparkles: Features
- Feature 1: Brief description 
- Feature 2: Brief description
- Feature 3: Brief description

## :bulb: Use Cases
**1. Predicting Cancellation Risk for Individual Reservations**
> Hotels can input upcoming reservations and receive a cancellation probability score for each booking. This helps staff proactively reach out to high-risk guests, send reminders, or require further confirmation

**2. Monthly and Seasonal Occupancy Forecasting**
> By aggregating and analyzing cancellation probabilities, hotels can generate more accurate occupancy forecasts for upcoming months or seasons. This can improve staffing/resource planning such as housekeeping schedules or inventory management.

**3. Revenue-at-Risk Estimation**
> By combining cancellation probabilities with reservation prices/costs, hotels can better estimate potential revenue loss. This allows managers to adjust pricing strategies, overbooking thresholds, or promotional offers. 

## :gear: Installation

The only requirement is a regular Python installation and then an integrated development environment (IDE) to make changes to the dataset if needed.

## :book: Example?

## :rocket: Usage


## :handshake: Contributing 


## :books: Documentation
Link to documentation: 


## :hourglass_flowing_sand: History
Updated on MONTH DAY 2026 Version XX.XX

## :page_facing_up: License
This project is not licensed for external use. All rights reserved.

## Running the modeling scripts

Place `hotel_bookings.csv` in the same folder as the Python scripts.

Run data preparation once, or again when the source dataset or cleaning logic changes:

```powershell
py .\prepare_data.py
```

Then run training, comparison, and evaluation:

```powershell
py .\train_model_clean_dataset_test.py
py .\compare_model_clean_dataset_test.py
py .\evaluate_model_clean_dataset_test.py
```

These scripts reuse `hotel_bookings_cleaned.csv`. Training saves the same trained Random Forest to MLflow and `hotel_cancellation_predictor.pkl`, without training it twice.

The evaluation script currently loads version 1 of `HotelCancellation` from the local MLflow database.