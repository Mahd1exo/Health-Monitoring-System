import matplotlib.pyplot as plt
from fuzzy_logic import body_temp, pulse_rate, spO2, severity

# Apply a dark background style for consistency
plt.style.use('dark_background')

def show_membership_functions(temp_input, pulse_input, spO2_input, severity_level):
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.patch.set_facecolor('#2E2E2E')  # Dark background for the figure

    # Body Temperature Membership Plot
    axs[0, 0].plot(body_temp.universe, body_temp['low'].mf, label='Low', color='cyan')
    axs[0, 0].plot(body_temp.universe, body_temp['normal'].mf, label='Normal', color='lime')
    axs[0, 0].plot(body_temp.universe, body_temp['high'].mf, label='High', color='magenta')
    axs[0, 0].axvline(x=temp_input, color='aqua', linestyle='--', label=f'Input: {temp_input}°C')
    axs[0, 0].set_title("Body Temperature (°C)", color='white')
    axs[0, 0].legend()
    axs[0, 0].tick_params(colors='white')

    # Pulse Rate Membership Plot
    axs[0, 1].plot(pulse_rate.universe, pulse_rate['low'].mf, label='Low', color='cyan')
    axs[0, 1].plot(pulse_rate.universe, pulse_rate['normal'].mf, label='Normal', color='lime')
    axs[0, 1].plot(pulse_rate.universe, pulse_rate['high'].mf, label='High', color='magenta')
    axs[0, 1].axvline(x=pulse_input, color='aqua', linestyle='--', label=f'Input: {pulse_input} BPM')
    axs[0, 1].set_title("Pulse Rate (BPM)", color='white')
    axs[0, 1].legend()
    axs[0, 1].tick_params(colors='white')

    # SpO₂ Level Membership Plot
    axs[1, 0].plot(spO2.universe, spO2['very_low'].mf, label='Very Low', color='cyan')
    axs[1, 0].plot(spO2.universe, spO2['low'].mf, label='Low', color='lime')
    axs[1, 0].plot(spO2.universe, spO2['normal'].mf, label='Normal', color='magenta')
    axs[1, 0].axvline(x=spO2_input, color='aqua', linestyle='--', label=f'Input: {spO2_input}%')
    axs[1, 0].set_title("SpO₂ Level (%)", color='white')
    axs[1, 0].legend()
    axs[1, 0].tick_params(colors='white')

    # Severity Level Membership Plot
    axs[1, 1].plot(severity.universe, severity['low'].mf, label='Low', color='cyan')
    axs[1, 1].plot(severity.universe, severity['medium'].mf, label='Medium', color='lime')
    axs[1, 1].plot(severity.universe, severity['high'].mf, label='High', color='magenta')
    axs[1, 1].plot(severity.universe, severity['very_high'].mf, label='Very High', color='red')
    axs[1, 1].axvline(x=severity_level, color='aqua', linestyle='--', label=f'Severity: {severity_level:.2f}')
    axs[1, 1].set_title("Severity Level", color='white')
    axs[1, 1].legend()
    axs[1, 1].tick_params(colors='white')

    plt.tight_layout()
    plt.show()
    
