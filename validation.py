from tkinter import messagebox
from style import ERROR_COLOR, ENTRY_BG_COLOR

BODY_TEMP_RANGE = (35, 42)  # Body temperature in Celsius
PULSE_RATE_RANGE = (40, 180)  # Pulse rate in BPM
SPO2_RANGE = (80, 100)  # SpO₂ level in percentage

def validate_inputs(body_temp, pulse_rate, spO2, entry_temp, entry_pulse, entry_spo2):
    # Reset background colors to default for each entry
    entry_temp.config(bg=ENTRY_BG_COLOR)
    entry_pulse.config(bg=ENTRY_BG_COLOR)
    entry_spo2.config(bg=ENTRY_BG_COLOR)
    
    # Body temperature validation
    if not (BODY_TEMP_RANGE[0] <= body_temp <= BODY_TEMP_RANGE[1]):
        message = (
            f"Body Temperature {body_temp}°C is too low. Expected minimum: {BODY_TEMP_RANGE[0]}°C."
            if body_temp < BODY_TEMP_RANGE[0] else
            f"Body Temperature {body_temp}°C is too high. Expected maximum: {BODY_TEMP_RANGE[1]}°C."
        )
        messagebox.showerror("Invalid Input", message)
        entry_temp.config(bg=ERROR_COLOR)  # Highlight entry if invalid
        return False

    # Pulse rate validation
    if not (PULSE_RATE_RANGE[0] <= pulse_rate <= PULSE_RATE_RANGE[1]):
        message = (
            f"Pulse Rate {pulse_rate} BPM is too low. Expected minimum: {PULSE_RATE_RANGE[0]} BPM."
            if pulse_rate < PULSE_RATE_RANGE[0] else
            f"Pulse Rate {pulse_rate} BPM is too high. Expected maximum: {PULSE_RATE_RANGE[1]} BPM."
        )
        messagebox.showerror("Invalid Input", message)
        entry_pulse.config(bg=ERROR_COLOR)  # Highlight entry if invalid
        return False

    # SpO₂ validation
    if not (SPO2_RANGE[0] <= spO2 <= SPO2_RANGE[1]):
        message = (
            f"SpO₂ Level {spO2}% is too low. Expected minimum: {SPO2_RANGE[0]}%."
            if spO2 < SPO2_RANGE[0] else
            f"SpO₂ Level {spO2}% is too high. Expected maximum: {SPO2_RANGE[1]}%."
        )
        messagebox.showerror("Invalid Input", message)
        entry_spo2.config(bg=ERROR_COLOR)  # Highlight entry if invalid
        return False

    return True
