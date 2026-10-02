###### DASHBOARD CREATOR ######


############################### IMPORT MODULES ##############################

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from Prediction import make_prediction
from datetime import datetime



####### DASHBOARD COLOR SCHEME ######
COLORS = {
    "navy": "#1E293B",
    "blue": "#2563EB",
    "blue_hover": "#1D4ED8",
    "background": "#F8FAFC",
    "white": "#FFFFFF",
    "green": "#16A34A",
    "red": "#DC2626",
    "gray": "#64748B",
    "light_gray": "#E2E8F0",
    "dark_text": "#0F172A"
}


# GLOBAL DATA

results_df = None



######################### DISPLAY RESULTS IN TABLE ####################################


def display_results(df):

    # Clear existing table
    for item in summary_table.get_children():
        summary_table.delete(item)

    # Add each reservation
    for _, row in df.iterrows():

        year = int(row["arrival_date_year"])
        month = row["arrival_date_month"]
        day = int(row["arrival_date_day_of_month"])

        # Convert date to day of week
        arrival_date = datetime.strptime(
            f"{year}-{month}-{day}",
            "%Y-%B-%d"
        )

        day_of_week = arrival_date.strftime("%A")

        probability = row["Cancellation Probability"]

        # Determine risk
        if probability < 50:

            risk = "Low Risk"
            tag = "low_probability"

        else:

            risk = "High Risk"
            tag = "high_probability"

        # Add row to table
        summary_table.insert(
            "",
            "end",
            values=(
                year,
                month,
                day,
                day_of_week,
                f"{probability:.1f}%",
                risk
            ),
            tags=(tag,)
        )



######### UPDATES SUMMARY CARDS #########
def update_summary(df):

    total = len(df)

    low_risk = (
        df["Cancellation Probability"] < 50
    ).sum()

    high_risk = (
        df["Cancellation Probability"] >= 50
    ).sum()

    total_value_label.config(
        text=str(total)
    )

    low_risk_value_label.config(
        text=str(low_risk)
    )

    high_risk_value_label.config(
        text=str(high_risk)
    )



############################ FILTER AND SORT FEATURES #############################################
def refresh_results(*args):

    if results_df is None:
        return

    # Start with all reservations
    filtered_df = results_df.copy()

    # FILTER

    selected_filter = filter_var.get()

    if selected_filter == "Low Risk":

        filtered_df = filtered_df[
            filtered_df["Cancellation Probability"] < 50
        ]

    elif selected_filter == "High Risk":

        filtered_df = filtered_df[
            filtered_df["Cancellation Probability"] >= 50
        ]


    # SORT
    selected_sort = sort_var.get()

    if selected_sort == "Highest Probability":

        filtered_df = filtered_df.sort_values(
            by="Cancellation Probability",
            ascending=False
        )

    elif selected_sort == "Lowest Probability":

        filtered_df = filtered_df.sort_values(
            by="Cancellation Probability",
            ascending=True
        )

    # Display filtered/sorted results
    display_results(filtered_df)

    # Update number currently displayed
    displayed_count_label.config(
        text=f"Showing {len(filtered_df)} of {len(results_df)} reservations"
    )



##################################### UPLOAD CSV #############################################
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


        # LOADING MESSAGE
        status_label.config(
            text="Analyzing reservations...",
            fg=COLORS["blue"]
        )

        root.update_idletasks()


        # READ CSV
        df = pd.read_csv(file_path)

        # CHECK REQUIRED COLUMNS
        required_columns = [
            "arrival_date_year",
            "arrival_date_month",
            "arrival_date_day_of_month"
        ]

        missing_columns = [
            column
            for column in required_columns
            if column not in df.columns
        ]

        if missing_columns:

            raise ValueError(
                f"Missing required columns: "
                f"{', '.join(missing_columns)}"
            )


        # RUN RANDOM FOREST
        probabilities = make_prediction(file_path)


        # CHECK PREDICTION COUNT
        if len(probabilities) != len(df):

            raise ValueError(
                f"The model returned "
                f"{len(probabilities)} predictions "
                f"for {len(df)} CSV rows."
            )


        # ADD PROBABILITY TO DATAFRAME
        df["Cancellation Probability"] = [
            probability * 100
            for probability in probabilities
        ]


        # SAVE RESULTS
        global results_df

        results_df = df

        # UPDATE FILE NAME

        file_label.config(
            text=f"Uploaded: {file_path.split('/')[-1]}"
        )


        # UPDATE SUMMARY
        update_summary(df)


        # RESET FILTERS
        filter_var.set("All")
        sort_var.set("Default")


        # DISPLAY RESULTS
        display_results(df)


        # UPDATE DISPLAY COUNT
        displayed_count_label.config(
            text=f"Showing {len(df)} of {len(df)} reservations"
        )


        # SUCCESS MESSAGE
        status_label.config(
            text=(
                f"✓ Analysis complete — "
                f"{len(df)} reservations analyzed"
            ),
            fg=COLORS["green"]
        )

    except Exception as e:

        status_label.config(
            text="Analysis failed",
            fg=COLORS["red"]
        )

        messagebox.showerror(
            "Prediction Error",
            str(e)
        )


########## CLEAR RESULTS #########

def clear_results():

    global results_df

    results_df = None

    # Clear table
    for item in summary_table.get_children():
        summary_table.delete(item)

    # Reset file information
    file_label.config(
        text="No file uploaded"
    )

    # Reset summary
    total_value_label.config(
        text="0"
    )

    low_risk_value_label.config(
        text="0"
    )

    high_risk_value_label.config(
        text="0"
    )

    # Reset displayed count
    displayed_count_label.config(
        text="Showing 0 reservations"
    )

    # Reset filters
    filter_var.set("All")
    sort_var.set("Default")

    # Reset status
    status_label.config(
        text="Ready to analyze reservations",
        fg=COLORS["gray"]
    )



##################################### DASHBOARD #############################################
root = tk.Tk()



########## WINDOW SETTINGS ##################

root.title(
    "Hotel Reservation Cancellation Predictor"
)

root.geometry(
    "1050x800"
)

root.minsize(
    900,
    650
)

root.configure(
    bg=COLORS["background"]
)


############################### TABLE STYLE ###############################

style = ttk.Style()
# Use a theme that allows custom Treeview colors
style.theme_use("clam")

style.configure(
    "Treeview",
    background=COLORS["white"],
    foreground=COLORS["dark_text"],
    fieldbackground=COLORS["white"],
    font=("Arial", 11),
    rowheight=34
)

style.configure(
    "Treeview.Heading",
    background=COLORS["navy"],
    foreground=COLORS["white"],
    font=("Arial", 12, "bold"),
    padding=8
)

style.map(
    "Treeview",
    background=[
        ("selected", "#DBEAFE")
    ],
    foreground=[
        ("selected", COLORS["dark_text"])
    ]
)


# TITLE
title_label = tk.Label(
    root,
    text="Hotel Reservation Cancellation Predictor",
    font=("Arial", 24, "bold"),
    bg=COLORS["navy"],
    fg=COLORS["white"]
)

title_label.pack(
    fill="x",
    pady=(0, 20),
    ipady=15
)


# BUTTON FRAME
button_frame = tk.Frame(
    root,
    bg=COLORS["background"]
)

button_frame.pack(
    pady=5
)


# UPLOAD BUTTON
upload_button = tk.Button(
    button_frame,
    text="Upload Reservation CSV",
    font=("Arial", 14, "bold"),
    bg=COLORS["blue"],
    fg=COLORS["white"],
    activebackground=COLORS["blue_hover"],
    activeforeground=COLORS["white"],
    padx=25,
    pady=10,
    relief="flat",
    borderwidth=0,
    cursor="hand2",
    command=upload_csv
)

upload_button.pack(
    side="left",
    padx=5
)


# CLEAR BUTTON
clear_button = tk.Button(
    button_frame,
    text="Clear Results",
    font=("Arial", 14, "bold"),
    bg=COLORS["light_gray"],
    fg=COLORS["dark_text"],
    activebackground="#CBD5E1",
    activeforeground=COLORS["dark_text"],
    padx=25,
    pady=10,
    relief="flat",
    borderwidth=0,
    cursor="hand2",
    command=clear_results
)

clear_button.pack(
    side="left",
    padx=5
)


###### FILE NAME FORMATTING ########
file_label = tk.Label(
    root,
    text="No file uploaded",
    font=("Arial", 14, "bold"),
    bg=COLORS["background"],
    fg=COLORS["navy"]
)

file_label.pack(
    pady=(12, 3)
)


###### CREATES STATUS MESSAGE ########
status_label = tk.Label(
    root,
    text="Ready to analyze reservations",
    font=("Arial", 11, "bold"),
    bg=COLORS["background"],
    fg=COLORS["gray"]
)

status_label.pack(
    pady=(0, 10)
)

############################### SUMMARY CARDS ###############################
summary_frame = tk.Frame(
    root,
    bg=COLORS["background"]
)

summary_frame.pack(
    fill="x",
    padx=30,
    pady=5
)


######  TOTAL RESERVATIONS SUMMARY ######
total_card = tk.Frame(
    summary_frame,
    bg=COLORS["white"],
    height = 40,
    highlightbackground=COLORS["light_gray"],
    highlightthickness=1
)

total_card.pack(
    side="left",
    fill="x",
    expand=True,
    padx=5
)

tk.Label(
    total_card,
    text="TOTAL RESERVATIONS",
    font=("Arial", 11, "bold"),
    bg=COLORS["white"],
    fg=COLORS["gray"]
).pack(
    pady=(10, 2)
)

total_value_label = tk.Label(
    total_card,
    text="0",
    font=("Arial", 22, "bold"),
    bg=COLORS["white"],
    fg=COLORS["navy"]
)

total_value_label.pack(
    pady=(0, 10)
)


###### LOW RISK SUMMARY ######

low_card = tk.Frame(
    summary_frame,
    bg=COLORS["white"],
    height = 40,
    highlightbackground=COLORS["light_gray"],
    highlightthickness=1
)

low_card.pack(
    side="left",
    fill="x",
    expand=True,
    padx=5
)

tk.Label(
    low_card,
    text="LOW RISK",
    font=("Arial", 11, "bold"),
    bg=COLORS["white"],
    fg=COLORS["green"]
).pack(
    pady=(10, 2)
)

low_risk_value_label = tk.Label(
    low_card,
    text="0",
    font=("Arial", 22, "bold"),
    bg=COLORS["white"],
    fg=COLORS["green"]
)

low_risk_value_label.pack(
    pady=(0, 10)
)

###### HIGH RISK SUMMARY ######
high_card = tk.Frame(
    summary_frame,
    bg=COLORS["white"],
    height = 40,
    highlightbackground=COLORS["light_gray"],
    highlightthickness=1
)

high_card.pack(
    side="left",
    fill="x",
    expand=True,
    padx=5
)

tk.Label(
    high_card,
    text="HIGH RISK",
    font=("Arial", 11, "bold"),
    bg=COLORS["white"],
    fg=COLORS["red"]
).pack(
    pady=(10, 2)
)

high_risk_value_label = tk.Label(
    high_card,
    text="0",
    font=("Arial", 22, "bold"),
    bg=COLORS["white"],
    fg=COLORS["red"]
)

high_risk_value_label.pack(
    pady=(0, 10)
)


############################### FILTER / SORTING ###############################

controls_frame = tk.Frame(
    root,
    bg=COLORS["background"]
)

controls_frame.pack(
    fill="x",
    padx=35,
    pady=(15, 5)
)


###### ADDS FILTER FEATURE ######

tk.Label(
    controls_frame,
    text="Filter:",
    font=("Arial", 11, "bold"),
    bg=COLORS["background"],
    fg=COLORS["dark_text"]
).pack(
    side="left"
)

filter_var = tk.StringVar(
    value="All"
)

filter_menu = ttk.Combobox(
    controls_frame,
    textvariable=filter_var,
    values=[
        "All",
        "Low Risk",
        "High Risk"
    ],
    state="readonly",
    width=15
)

filter_menu.pack(
    side="left",
    padx=(5, 25)
)

filter_menu.bind(
    "<<ComboboxSelected>>",
    refresh_results
)


###### ADDS SORTING FEATURE ######

tk.Label(
    controls_frame,
    text="Sort:",
    font=("Arial", 11, "bold"),
    bg=COLORS["background"],
    fg=COLORS["dark_text"]
).pack(
    side="left"
)

sort_var = tk.StringVar(
    value="Default"
)

sort_menu = ttk.Combobox(
    controls_frame,
    textvariable=sort_var,
    values=[
        "Default",
        "Highest Probability",
        "Lowest Probability"
    ],
    state="readonly",
    width=20
)

sort_menu.pack(
    side="left",
    padx=5
)

sort_menu.bind(
    "<<ComboboxSelected>>",
    refresh_results
)


###### DISPLAYS COUNTS ######

displayed_count_label = tk.Label(
    controls_frame,
    text="Showing 0 reservations",
    font=("Arial", 10),
    bg=COLORS["background"],
    fg=COLORS["gray"]
)

displayed_count_label.pack(
    side="right"
)


###### CREATES TABLE TITLE ######

table_title = tk.Label(
    root,
    text="Reservation Cancellation Summary",
    font=("Arial", 18, "bold"),
    bg=COLORS["background"],
    fg=COLORS["dark_text"]
)

table_title.pack(
    pady=(10, 10)
)


###### CREATES TABLE FRAME ######

table_frame = tk.Frame(
    root,
    bg=COLORS["white"],
    highlightbackground=COLORS["light_gray"],
    highlightthickness=1
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=(0, 10)
)


###### CREATES TABLE SCROLLBAR ######

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical"
)

scrollbar.pack(
    side="right",
    fill="y"
)



########################## CREATES SUMMARY TABLE ################3########

columns = (
    "arrival_date_year",
    "arrival_date_month",
    "arrival_date_day_of_month",
    "Day of Week",
    "Cancellation Probability",
    "Risk"
)

summary_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    yscrollcommand=scrollbar.set
)

scrollbar.config(
    command=summary_table.yview
)


###### CREATES COLUMN HEADINGS ######

summary_table.heading(
    "arrival_date_year",
    text="Arrival Year"
)

summary_table.heading(
    "arrival_date_month",
    text="Arrival Month"
)

summary_table.heading(
    "arrival_date_day_of_month",
    text="Arrival Day"
)

summary_table.heading(
    "Day of Week",
    text="Day of Week"
)

summary_table.heading(
    "Cancellation Probability",
    text="Cancellation Probability"
)

summary_table.heading(
    "Risk",
    text="Risk"
)



###### FORMATS COLUMN WIDTHS ######

summary_table.column(
    "arrival_date_year",
    width=110,
    anchor="center"
)

summary_table.column(
    "arrival_date_month",
    width=120,
    anchor="center"
)

summary_table.column(
    "arrival_date_day_of_month",
    width=110,
    anchor="center"
)

summary_table.column(
    "Day of Week",
    width=120,
    anchor="center"
)

summary_table.column(
    "Cancellation Probability",
    width=210,
    anchor="center"
)

summary_table.column(
    "Risk",
    width=120,
    anchor="center"
)



###### SETS RISK TAG COLORS ######
summary_table.tag_configure(
    "low_probability",
    foreground=COLORS["green"]
)

summary_table.tag_configure(
    "high_probability",
    foreground=COLORS["red"]
)


summary_table.pack(
    fill="both",
    expand=True
)


###### RISK LEGEND ######

legend_frame = tk.Frame(
    root,
    bg=COLORS["background"]
)

legend_frame.pack(
    pady=(5, 15)
)

###### CREATES LOW RISK LEGEND ######

low_risk_label = tk.Label(
    legend_frame,
    text="● Low Risk (<50%)",
    font=("Arial", 12, "bold"),
    bg=COLORS["background"],
    fg=COLORS["green"]
)

low_risk_label.pack(
    side="left",
    padx=20
)


###### CREATES HIGH RISK LEGEND ######

high_risk_label = tk.Label(
    legend_frame,
    text="● High Risk (≥50%)",
    font=("Arial", 12, "bold"),
    bg=COLORS["background"],
    fg=COLORS["red"]
)

high_risk_label.pack(
    side="left",
    padx=20
)



###### START DASHBOARD ######

root.mainloop()
