
import tkinter as tk
from tkinter import messagebox
import math

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from electricity_predictor import train_model, predict_for_date


# Train the machine learning model
(
    model,
    mae,
    test_dates,
    actual_values,
    predicted_values,
    first_date,
    last_date
) = train_model()


# Create the main window
root = tk.Tk()
root.title("Electricity Bill Predictor")
root.geometry("1200x750")
root.minsize(1000, 650)


# Main heading
title = tk.Label(
    root,
    text="Electricity Bill Predictor",
    font=("Arial", 24, "bold")
)
title.pack(pady=15)

subtitle = tk.Label(
    root,
    text="Predict daily electricity consumption and estimate your bill",
    font=("Arial", 12)
)
subtitle.pack(pady=5)


# Main content frame
main_frame = tk.Frame(root)
main_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=15
)


# Left section
left_frame = tk.Frame(main_frame, width=350)
left_frame.pack(
    side="left",
    fill="y",
    padx=15
)

left_frame.pack_propagate(False)


# Right section
right_frame = tk.Frame(main_frame)
right_frame.pack(
    side="right",
    fill="both",
    expand=True,
    padx=15
)


# Input heading
date_heading = tk.Label(
    left_frame,
    text="Enter Prediction Details",
    font=("Arial", 16, "bold")
)
date_heading.pack(pady=15)


# Day input
tk.Label(
    left_frame,
    text="Day (1-31)",
    font=("Arial", 11)
).pack(pady=5)

day_entry = tk.Entry(
    left_frame,
    justify="center",
    font=("Arial", 12)
)
day_entry.pack(pady=5)


# Month input
tk.Label(
    left_frame,
    text="Month (1-12)",
    font=("Arial", 11)
).pack(pady=5)

month_entry = tk.Entry(
    left_frame,
    justify="center",
    font=("Arial", 12)
)
month_entry.pack(pady=5)


# Year input
tk.Label(
    left_frame,
    text="Year",
    font=("Arial", 11)
).pack(pady=5)

year_entry = tk.Entry(
    left_frame,
    justify="center",
    font=("Arial", 12)
)
year_entry.pack(pady=5)


# Electricity rate input
tk.Label(
    left_frame,
    text="Electricity Rate (Rs. per kWh)",
    font=("Arial", 11)
).pack(pady=5)

rate_entry = tk.Entry(
    left_frame,
    justify="center",
    font=("Arial", 12)
)
rate_entry.pack(pady=5)


# Result display
result_label = tk.Label(
    left_frame,
    text="Your prediction will appear here.",
    font=("Arial", 11),
    justify="left",
    wraplength=320
)
result_label.pack(pady=20)


# Prediction function
def predict():

    try:
        # Get values entered by the user
        day = int(day_entry.get())
        month = int(month_entry.get())
        year = int(year_entry.get())
        rate = float(rate_entry.get())

        # Validate electricity rate
        if not math.isfinite(rate) or rate <= 0:
            messagebox.showerror(
                "Invalid Input",
                "Please enter an electricity rate greater than zero."
            )
            return

        # Get prediction
        selected_date, consumption = predict_for_date(
            day,
            month,
            year,
            model
        )

        # Calculate estimated energy charge
        estimated_bill = consumption * rate

        # Display results
        result_label.config(
            text=(
                f"Prediction Date:\n"
                f"{selected_date.strftime('%d-%m-%Y')}\n\n"
                f"Predicted Consumption:\n"
                f"{consumption:.2f} kWh\n\n"
                f"Electricity Rate:\n"
                f"Rs. {rate:.2f} per kWh\n\n"
                f"Estimated Energy Charge:\n"
                f"Rs. {estimated_bill:.2f}\n\n"
                f"Model MAE:\n"
                f"{mae:.2f} kWh"
            )
        )

        # Warn about dates outside the dataset
        if selected_date.date() > last_date.date():
            messagebox.showwarning(
                "Forecast Limitation",
                "This date is after the historical dataset. "
                "The prediction may be less reliable."
            )

        elif selected_date.date() < first_date.date():
            messagebox.showwarning(
                "Forecast Limitation",
                "This date is before the historical dataset. "
                "The prediction may be less reliable."
            )

    except (ValueError, OverflowError):
        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid date and electricity rate."
        )

    except Exception as error:
        messagebox.showerror(
            "Error",
            str(error)
        )


# Prediction button
predict_button = tk.Button(
    left_frame,
    text="Predict Electricity Bill",
    font=("Arial", 12, "bold"),
    command=predict
)
predict_button.pack(pady=10)


# Disclaimer
disclaimer = tk.Label(
    left_frame,
    text=(
        "Estimated energy charge only.\n"
        "GST, fixed charges and other applicable charges are excluded."
    ),
    font=("Arial", 9),
    fg="gray",
    wraplength=320,
    justify="center"
)
disclaimer.pack(pady=15)


# Exit button
exit_button = tk.Button(
    left_frame,
    text="Exit",
    command=root.destroy
)
exit_button.pack(pady=10)


# Graph heading
graph_heading = tk.Label(
    right_frame,
    text="Actual vs Predicted Electricity Consumption",
    font=("Arial", 15, "bold")
)
graph_heading.pack(pady=10)


# Create graph
figure = Figure(
    figsize=(7, 5),
    dpi=100
)

axis = figure.add_subplot(111)

axis.plot(
    test_dates,
    actual_values,
    label="Actual Consumption"
)

axis.plot(
    test_dates,
    predicted_values,
    label="Predicted Consumption"
)

axis.set_title("Electricity Consumption Comparison")
axis.set_xlabel("Date")
axis.set_ylabel("Consumption (kWh)")

axis.legend()
axis.tick_params(axis="x", rotation=45)

figure.tight_layout()


# Embed graph inside Tkinter
canvas = FigureCanvasTkAgg(
    figure,
    master=right_frame
)

canvas.draw()

canvas.get_tk_widget().pack(
    fill="both",
    expand=True
)


# Keep the application running
root.mainloop()
