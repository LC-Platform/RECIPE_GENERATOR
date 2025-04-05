# 🌐 Flutter + Flask Web App

This project integrates a **Flutter frontend** (with web support) with a **Flask backend** that features data analysis and visualization. It provides a seamless way to build cross-platform apps while leveraging Python's backend capabilities.

---

## 📦 Prerequisites

### 🔹 Flutter Setup

1. **Install Flutter** via Visual Studio Code Extensions.
2. **SDK Setup**:
   - If Flutter is not installed yet, click **Download SDK**.
   - If already installed, click **Locate SDK**.
3. **Configure Flutter** by running the following commands in your terminal:

   ```bash
   flutter doctor
   flutter config --enable-web
   flutter pub get
   flutter run -d chrome
flutter doctor: Checks that your environment is set up correctly.

flutter config --enable-web: Enables web support.

flutter pub get: Downloads the necessary dependencies listed in your pubspec.yaml.

flutter run -d chrome: Launches your app in the Chrome browser.

### 🔹 Backend Setup (Flask)

Ensure Python 3 is installed.

Upgrade pip:
```bash
python3 -m pip install --upgrade pip
```

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Application

### ▶️ Frontend (Flutter)

Run your Flutter web app with:
```bash
flutter run -d chrome
```

### ▶️ Backend (Flask)

Start the Flask server with:
```bash
python main.py
```
