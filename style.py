# style.py

# Tkinter GUI style settings for a dark theme

# Background colors
BACKGROUND_COLOR = "#2E2E2E"
ENTRY_BG_COLOR = "#2E2E2E"
BUTTON_BG_COLOR = "#404040"
TEXT_COLOR = "white"
ERROR_COLOR = "lightcoral"
STATUS_COLOR_NORMAL = "green"
STATUS_COLOR_WARNING = "yellow"
STATUS_COLOR_HIGH = "orange"
STATUS_COLOR_VERY_HIGH = "red"

# Font settings
FONT = ("Helvetica", 10)
FONT_BOLD = ("Helvetica", 10, "bold")
STATUS_FONT = ("Helvetica", 12, "bold")

# Apply theme settings to an entry widget
def apply_entry_style(entry_widget, is_valid=True):
    entry_widget.config(
        bg=ENTRY_BG_COLOR if is_valid else ERROR_COLOR,
        fg=TEXT_COLOR,
        insertbackground=TEXT_COLOR,
        relief="groove",
        font=FONT
    )

# Apply style to the main status label
def apply_status_label_style(label_widget):
    label_widget.config(
        font=STATUS_FONT,
        fg=TEXT_COLOR,
        bg=BACKGROUND_COLOR
    )

# Apply button style
def apply_button_style(button_widget):
    button_widget.config(
        bg=BUTTON_BG_COLOR,
        fg=TEXT_COLOR,
        font=FONT_BOLD,
        relief="groove",
        bd=2
    )

# Function to get color based on severity level
def get_severity_color(severity_level):
    if severity_level >= 80:
        return STATUS_COLOR_VERY_HIGH
    elif severity_level >= 60:
        return STATUS_COLOR_HIGH
    elif severity_level >= 30:
        return STATUS_COLOR_WARNING
    else:
        return STATUS_COLOR_NORMAL
