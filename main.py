import tkinter as tk
from tkinter import messagebox
import requests  # For sending HTTP requests to the Go service
import threading
from validation import validate_inputs
from fuzzy_logic import run_fuzzy_logic
from plotting import show_membership_functions
from style import (
    BACKGROUND_COLOR,
    apply_entry_style,
    apply_status_label_style,
    apply_button_style,
    get_severity_color
)

# Function to get health suggestion from the Go service
def get_health_suggestion_from_go_service(temp, pulse, spO2, language="English"):
    url = "http://localhost:8080/suggest"  # Go service endpoint
    payload = {
        "temp": temp,
        "pulse": pulse,
        "spO2": spO2,
        "language": language
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Check for HTTP request errors
        suggestion = response.json().get("suggestion", "No suggestion available")
        return suggestion
    except requests.exceptions.RequestException as e:
        print(f"Error contacting suggestion service: {e}")
        return "Suggestion service is unavailable."
    

def show_suggestion_window(suggestion):
    suggestion_window = tk.Toplevel(root)
    suggestion_window.title("Health Suggestion")
    suggestion_window.configure(bg=BACKGROUND_COLOR)

    fixed_width = 500  
    wrap_length = fixed_width - 50  

    text_length = len(suggestion)
    line_height = 20  
    dynamic_height = max(200, min((text_length // 60 + 1) * line_height, 600))  

    suggestion_window.geometry(f"{fixed_width}x{dynamic_height}")

    tk.Label(suggestion_window, text="Health Suggestion", font=("Helvetica", 14, "bold"),
             bg=BACKGROUND_COLOR, fg="white").pack(pady=10)

    tk.Label(suggestion_window, text=suggestion, font=("Helvetica", 10), bg=BACKGROUND_COLOR,
             fg="white", wraplength=wrap_length, justify="left").pack(pady=10)


    tk.Button(suggestion_window, text="Close", command=suggestion_window.destroy, bg="#404040",
              fg="white", font=("Helvetica", 10, "bold")).pack(pady=10)



def run_and_display():
    try:
        temp_input = float(entry_temp.get())
        pulse_input = float(entry_pulse.get())
        spO2_input = float(entry_spo2.get())
        
        # Validate inputs
        if not validate_inputs(temp_input, pulse_input, spO2_input, entry_temp, entry_pulse, entry_spo2):
            return

        # Run fuzzy logic and capture the results
        severity_level, alert_message, alert_color = run_fuzzy_logic(temp_input, pulse_input, spO2_input)

        # If no severity level is calculated, show an error message
        if severity_level is None:
            messagebox.showerror("Calculation Error", alert_message)
            status_label.config(text="Severity Level\n Not calculated - No matching rule.", fg=alert_color)
            return

        # Update status label with severity level and message
        status_label.config(text=f"Severity Level: {severity_level:.2f}\n{alert_message}", fg=get_severity_color(severity_level))

        # Display membership function plots in the main thread
        plot_thread = threading.Thread(target=show_membership_functions, args=(temp_input, pulse_input, spO2_input, severity_level))
        plot_thread.start()

        # Get the health suggestion in a separate thread to avoid blocking
        def fetch_and_show_suggestion():
            suggestion = get_health_suggestion_from_go_service(temp_input, pulse_input, spO2_input)
            show_suggestion_window(suggestion)

        suggestion_thread = threading.Thread(target=fetch_and_show_suggestion)
        suggestion_thread.start()

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numerical values for all inputs.")

# GUI setup
root = tk.Tk()
root.title("Health Monitoring System")
root.configure(bg=BACKGROUND_COLOR)

status_label = tk.Label(root, text="Severity Level \nNot calculated")
apply_status_label_style(status_label)
status_label.grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(root, text="Body Temperature (°C):", fg="white", bg=BACKGROUND_COLOR).grid(row=1, column=0, padx=10, pady=10)
entry_temp = tk.Entry(root)
apply_entry_style(entry_temp)
entry_temp.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Pulse Rate (BPM):", fg="white", bg=BACKGROUND_COLOR).grid(row=2, column=0, padx=10, pady=10)
entry_pulse = tk.Entry(root)
apply_entry_style(entry_pulse)
entry_pulse.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="SpO₂ Level (%):", fg="white", bg=BACKGROUND_COLOR).grid(row=3, column=0, padx=10, pady=10)
entry_spo2 = tk.Entry(root)
apply_entry_style(entry_spo2)
entry_spo2.grid(row=3, column=1, padx=10, pady=10)

evaluate_button = tk.Button(root, text="Evaluate Health Status", command=run_and_display)
apply_button_style(evaluate_button)
evaluate_button.grid(row=4, column=0, columnspan=2, pady=20)

root.mainloop()
