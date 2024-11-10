# openai_suggestions.py
import openai
from tkinter import messagebox

# Set your OpenAI API key
openai.api_key = "sk-XXXXXXXX"

def get_health_suggestion(temp, pulse, spO2, language="Persian"):
    # Formulate the prompt with language specification
    messages = [
        {"role": "system", "content": "You are a health monitoring assistant."},
        {
            "role": "user",
            "content": f"""
            A patient has the following health readings:
            - Body Temperature: {temp}°C
            - Pulse Rate: {pulse} BPM
            - SpO₂ Level: {spO2}%

            Based on these values, please provide a health assessment and any recommendations in {language}, focusing on the potential severity of the readings and any medical advice.
            """
        },
    ]

    # Generate a chat completion
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Extract the assistant's reply
    suggestion = chat.choices[0].message.content.strip()
    return suggestion

def show_suggestion_alert(temp, pulse, spO2, language="Persian"):
    try:
        # Get the health suggestion in Persian from the OpenAI chat model
        suggestion = get_health_suggestion(temp, pulse, spO2, language)
        
        # Show the suggestion in a Tkinter alert window
        messagebox.showinfo(f"Health Suggestion ({language})", suggestion)
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get suggestion: {e}")