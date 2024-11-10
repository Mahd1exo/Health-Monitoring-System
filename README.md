
# 🏥 Health Monitoring System with Fuzzy Logic 🧠

The **Health Monitoring System** is a cross-platform application utilizing Python, Go, and Rust for real-time health assessment and insights. It evaluates a patient's health based on vital signs such as body temperature, pulse rate, and SpO₂ level using fuzzy logic, and provides health suggestions powered by either OpenAI or Google GenAI.
![Screenshot 2024-11-10 030921](https://github.com/user-attachments/assets/ffdd1e64-5c23-430c-85ab-afa2fb0bafa2)

---

## 📑 Table of Contents

- [✨ Features](#features)
- [📐 Architecture](#architecture)
- [📋 Prerequisites](#prerequisites)
- [⚙️ Installation](#installation)
- [🚀 Usage](#usage)
- [🗂 Code Structure](#code-structure)
- [📊 Example Scenarios](#example-scenarios)
- [🔮 Future Enhancements](#future-enhancements)
- [🤝 Contributing](#contributing)
- [📜 License](#license)

---

## ✨ Features

- **Fuzzy Logic-based Health Assessment** 🧩: Determines severity levels from low to very high based on body temperature, pulse rate, and SpO₂ level.
- **Dynamic GUI** 💻: Built with Tkinter, the GUI provides an interactive interface with real-time input validation, severity alerts, and plots.
- **AI-Powered Health Suggestions** 🧠: Fetches health insights through Go and Rust-based backend APIs that communicate with either OpenAI or Google GenAI APIs, allowing flexibility.
- **Concurrent Display of Charts & Suggestions** 📈: Uses Python’s threading to show both charts and AI-generated suggestions simultaneously.
- **Cross-Platform Integration** 🔗: Combines Python, Go, and Rust for an optimized and modular system.
- **Error Handling** ⚠️: Alerts for out-of-range inputs, rule mismatches, and API connectivity issues.

---

## 📐 Architecture

This project follows a **multi-language client-server architecture**:

1. **Frontend (Python)** 🐍: The Python-based Tkinter GUI captures user inputs, validates them, and uses fuzzy logic to determine a severity level. It then displays a plot of membership functions and communicates with the backend for AI-based health suggestions.

2. **Backend (Go & Rust)** 🦾: The backend APIs (available in both Go and Rust) handle requests from the frontend and fetch health suggestions from either OpenAI or Google GenAI based on the selected provider. The backend ensures smooth and secure communication with these AI services.

---

## 📋 Prerequisites

- **Python 3.x** 🐍
- **Go 1.16+** 🐹
- **Rust** 🦀
- **OpenAI or GenAI API Key** 🔑
- **Docker** 🐳 (optional, for containerized deployment)

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Mahd1exo/health-monitoring-system.git
cd health-monitoring-system
```

### 2. Python Setup

Install Python dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Go and Rust Setup

To install dependencies for the backend:

- **Go**: Ensure the Actix Web, Reqwest, and Serde crates are configured in your `Cargo.toml`.
- **Rust**: Set up your project with `cargo init` and add dependencies.

Or, if using Docker, build the container with:

```bash
docker build -t health_suggestion_service .
docker run -p 8080:8080 health_suggestion_service
```

---

## 🚀 Usage

### 1. Start the Python Application

Run the Python GUI:

```bash
python main.py
```

### 2. Input Data

In the GUI, enter values for:
- **Body Temperature (°C)**
- **Pulse Rate (BPM)**
- **SpO₂ Level (%)**

### 3. AI Suggestion

Choose either **OpenAI** or **GenAI** for health suggestions. The AI model will analyze the inputs and display an immediate suggestion alongside the fuzzy logic assessment.

---

## 🗂 Code Structure

The project is organized into modular components for easy maintenance and extensibility:

```
health-monitoring-system/
├── main.py                 # Main Python GUI and fuzzy logic controller
├── ai_suggestion_go/       # Go backend API for health suggestions
    ├── go.mod
    └── main.go
├── ai_suggestion_rust/      # Rust backend API for health suggestions
    ├── Cargo.toml
    └── src
        └── main.rs
├── fuzzy_logic.py          # Fuzzy logic calculations and rules
├── validation.py           # Input validation functions
├── plotting.py             # Plotting membership functions
├── style.py                # GUI style settings
├── openai_suggestions.py   # OpenAI API for health suggestions
├── suggestion_service.go   # Go backend API for health suggestions
└── README.txt              # Documentation
```

---

## 📊 Example Scenarios

1. **Normal Condition** 🟢:
   - **Inputs**: Body Temp: 37°C, Pulse: 80 BPM, SpO₂: 98%
   - **Result**: Low severity, stable condition.

2. **Medium Severity** 🟠:
   - **Inputs**: Body Temp: 38.5°C, Pulse: 95 BPM, SpO₂: 90%
   - **Result**: Medium severity, monitor condition.

3. **High Severity (Critical)** 🔴:
   - **Inputs**: Body Temp: 40°C, Pulse: 48 BPM, SpO₂: 84%
   - **Result**: Very high severity, seek immediate medical attention.

---

## 🔮 Future Enhancements

Potential future improvements:

- **Historical Data Logging** 📜: Save and review past health assessments.
- **Additional Rules & Customizations** ⚙️: Enhance rule complexity for nuanced assessments.
- **Web & Mobile Versions** 📱: Expand accessibility beyond desktop environments.
- **Multi-Language Support** 🌍: Offer UI translations for non-English users.

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. **Fork** the repository.
2. **Create** a new branch (e.g., `feature-branch`).
3. **Commit** your changes.
4. **Push** the branch.
5. **Open** a Pull Request.

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

Feel free to explore and customize the **Health Monitoring System** for more personalized health assessments! 🩺💡
