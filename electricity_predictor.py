
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


def train_model():

    # Load historical electricity data
    data = pd.read_csv("daily_electricity.csv")

    # Convert Day column into datetime format
    data["Day"] = pd.to_datetime(data["Day"])

    # Create date-related features
    data["Day_of_Month"] = data["Day"].dt.day
    data["Month"] = data["Day"].dt.month
    data["Day_of_Week"] = data["Day"].dt.day_of_week

    # Select input features and target
    X = data[
        ["Day_of_Month", "Month", "Day_of_Week"]
    ]

    y = data["Daily_Consumption_kWh"]

    # Split data chronologically (80% training, 20% testing)
    split_index = int(len(X) * 0.8)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    # Create and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict test data
    y_pred = model.predict(X_test)

    # Calculate Mean Absolute Error
    mae = mean_absolute_error(y_test, y_pred)

    # Train final model using all historical data
    final_model = LinearRegression()
    final_model.fit(X, y)

    return (
        final_model,
        mae,
        data["Day"].iloc[split_index:],
        y_test,
        y_pred,
        data["Day"].min(),
        data["Day"].max()
    )


def predict_for_date(day, month, year, model):

    # Create the selected date
    selected_date = pd.Timestamp(
        year=year,
        month=month,
        day=day
    )

    # Prepare input features
    user_input = pd.DataFrame({
        "Day_of_Month": [selected_date.day],
        "Month": [selected_date.month],
        "Day_of_Week": [selected_date.dayofweek]
    })

    # Predict electricity consumption
    predicted_consumption = model.predict(user_input)[0]

    # Consumption cannot be negative
    predicted_consumption = max(0, predicted_consumption)

    return selected_date, predicted_consumption
