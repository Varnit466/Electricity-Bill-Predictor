# Electricity Bill Predictor

## Project Overview
The Electricity Bill Predictor is a machine learning project that predicts daily household electricity consumption and estimates the corresponding electricity energy charge.

The project uses historical electricity consumption data and a Linear Regression model to make predictions.

## Features
- Predicts daily electricity consumption in kWh.
- Estimates electricity energy charges using a user-provided rate per kWh.
- Displays actual vs predicted consumption in a graph.
- Provides a graphical user interface using Tkinter.
- Evaluates model performance using Mean Absolute Error (MAE).

## Technologies Used
- Python
- Pandas
- Scikit-learn
- Matplotlib
- Tkinter

## Dataset
The project uses the UCI Individual Household Electric Power Consumption dataset.

Source: https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption

The original dataset was processed to calculate daily electricity consumption in kWh.

## Machine Learning Model
Linear Regression is used to predict daily electricity consumption.

The model uses date-related features:
- Day of the month
- Month
- Day of the week

The dataset is divided chronologically into 80% training data and 20% testing data.

Model performance is evaluated using Mean Absolute Error (MAE).

## How to Run
1. Install the required libraries:
   `pip install pandas scikit-learn matplotlib`
2. Keep `electricity_predictor.py`, `electricity_gui.py`, and `daily_electricity.csv` in the same folder.
3. Run:
   `python electricity_gui.py`

## Limitations
- Predictions are based on historical consumption patterns.
- Predictions outside the historical dataset may be less reliable.
- The estimated energy charge excludes GST, fixed charges, and other applicable charges.
- Actual electricity bills may differ depending on the tariff structure.

## Author
Varnit Agarwal
