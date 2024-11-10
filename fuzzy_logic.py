import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Define fuzzy variables and membership functions (same as original)
body_temp = ctrl.Antecedent(np.arange(35, 42, 0.1), 'body_temp')
pulse_rate = ctrl.Antecedent(np.arange(40, 180, 1), 'pulse_rate')
spO2 = ctrl.Antecedent(np.arange(80, 101, 1), 'spO2')
severity = ctrl.Consequent(np.arange(0, 101, 1), 'severity')

# Define membership functions
body_temp['low'] = fuzz.trimf(body_temp.universe, [35, 36, 37])
body_temp['normal'] = fuzz.trimf(body_temp.universe, [36, 37, 38])
body_temp['high'] = fuzz.trimf(body_temp.universe, [37, 39, 41])

pulse_rate['low'] = fuzz.trimf(pulse_rate.universe, [40, 60, 80])
pulse_rate['normal'] = fuzz.trimf(pulse_rate.universe, [70, 100, 130])
pulse_rate['high'] = fuzz.trimf(pulse_rate.universe, [120, 140, 180])

spO2['very_low'] = fuzz.trimf(spO2.universe, [80, 85, 90])
spO2['low'] = fuzz.trimf(spO2.universe, [88, 92, 95])
spO2['normal'] = fuzz.trimf(spO2.universe, [94, 97, 100])

severity['low'] = fuzz.trimf(severity.universe, [0, 25, 50])
severity['medium'] = fuzz.trimf(severity.universe, [30, 50, 70])
severity['high'] = fuzz.trimf(severity.universe, [60, 80, 90])
severity['very_high'] = fuzz.trimf(severity.universe, [80, 90, 100])

# Define rules
rules = [
    ctrl.Rule(body_temp['high'] & pulse_rate['low'] & spO2['very_low'], severity['very_high']),
    ctrl.Rule(body_temp['high'] & pulse_rate['low'] & spO2['low'], severity['high']),
    ctrl.Rule(body_temp['normal'] & pulse_rate['low'] & spO2['low'], severity['high']),
    ctrl.Rule(body_temp['normal'] & pulse_rate['normal'] & spO2['low'], severity['medium']),
    ctrl.Rule(body_temp['normal'] & pulse_rate['normal'] & spO2['normal'], severity['low']),
    ctrl.Rule(body_temp['low'] & pulse_rate['low'] & spO2['low'], severity['high']),
    ctrl.Rule(body_temp['low'] & pulse_rate['normal'] & spO2['very_low'], severity['very_high']),
]

# Control system setup
health_monitoring_ctrl = ctrl.ControlSystem(rules)
health_monitoring = ctrl.ControlSystemSimulation(health_monitoring_ctrl)

def run_fuzzy_logic(temp_input, pulse_input, spO2_input):
    # Set the inputs for the fuzzy system
    health_monitoring.input['body_temp'] = temp_input
    health_monitoring.input['pulse_rate'] = pulse_input
    health_monitoring.input['spO2'] = spO2_input

    # Try to compute the fuzzy system output, with error handling if no rule matches
    try:
        health_monitoring.compute()
        severity_level = health_monitoring.output.get('severity', None)

        if severity_level is None:
            return None, "No matching rule found. Unable to calculate severity level.", "white"

        # Determine alert details based on the severity level
        if severity_level >= 80:
            return severity_level, "ALERT: Very High severity! \nImmediate medical attention recommended", "red"
        elif severity_level >= 60:
            return severity_level, "Warning: High severity. \nMonitor patient closely", "orange"
        elif severity_level >= 30:
            return severity_level, "Warning: Medium severity. \nCheck condition regularly", "yellow"
        else:
            return severity_level, "Normal: Low severity. \nPatient condition is stable", "green"

    except Exception as e:
        return None, f"Error calculating severity: {str(e)}", "white"
