import tkinter as tk
from tkinter import filedialog, messagebox

from Prediction import make_prediction


def upload_csv():

    file_path = filedialog.askopenfilename(
        title="Select Reservation CSV",
        filetypes=[
            ("CSV files", "*.csv"),
            ("All files", "*.*")
        ]
    )

    if not file_path:
        return

    try:

        # Run the Random Forest
        probabilities = make_prediction(file_path)

        # Get prediction for the first reservation
        probability = probabilities[0]

        # Convert to percentage
        percentage = probability * 100

        # Update result
        result_label.config(
            text=f"{percentage:.1f}%",
            fg="green"
        )

        # Show filename
        file_label.config(
            text=f"Uploaded: {file_path.split('/')[-1]}"
        )

    except Exception as e:

        messagebox.showerror(
            "Prediction Error",
            str(e)
        )


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

root = tk.Tk()

root.title("Hotel Reservation Cancellation Predictor")
root.geometry("850x450")

root.configure(bg="white")


# Title
title_label = tk.Label(
    root,
    text="Hotel Reservation Cancellation Predictor",
    font=("Arial", 24, "bold"),
    bg="white",
    fg="black"
)

title_label.pack(pady=(30, 25))


# Upload button
upload_button = tk.Button(
    root,
    text="Upload Reservation CSV",
    font=("Arial", 16, "bold"),
    bg="#2F80ED",
    fg="white",
    padx=25,
    pady=12,
    command=upload_csv
)

upload_button.pack()


# File information
file_label = tk.Label(
    root,
    text="No file uploaded",
    font=("Arial", 12),
    bg="white",
    fg="gray"
)

file_label.pack(pady=15)


# Prediction explanation
message_label = tk.Label(
    root,
    text=(
        "Based on your input, the probability that "
        "the reservation will be cancelled is"
    ),
    font=("Arial", 18),
    bg="white",
    fg="black"
)

message_label.pack(pady=(35, 10))


# Prediction result
result_label = tk.Label(
    root,
    text="--",
    font=("Arial", 36, "bold"),
    bg="white",
    fg="green"
)

result_label.pack()


# Start dashboard
root.mainloop()