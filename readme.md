# Hospital Appointment Booking System (HABS)

This is a Hospital Appointment Booking System (HABS) built with Python and PySide6. The application allows users to sign up, log in, and manage their medical appointments, including selecting symptoms and viewing appointments in a calendar format.

## Features

- **User Registration & Login:** Secure sign-up and login with validation for email, phone, postal code, and password strength.
- **Appointment Booking:** Users can book appointments by selecting date, time, and symptoms.
- **Symptom Selection:** Choose from categorized symptoms, which affect appointment severity and scheduling.
- **Calendar View:** View all appointments in a monthly calendar.
- **Edit & Delete Appointments:** Modify or remove existing appointments.
- **Settings:** Change username and password.
- **Persistent Data:** User and appointment data are stored in JSON files.

## File Structure

- `project.py` — Main application code (UI and logic).
- `data.json` — Stores user data.
- `appointments.json` — Stores appointment data per user.
- `symptoms.json` — List of symptoms and their severity.
- `postal_codes.csv` — Canadian postal code validation.
- `main.qss`, `calender.qss`, `symptoms.qss`, `view.qss` — Stylesheets for the UI.
- `readme.md` — This file.

## Requirements

- Python 3.8+
- [PySide6](https://pypi.org/project/PySide6/)

## How to Run

1. **Install dependencies:**
    ```sh
    pip install PySide6
    ```

2. **Run the application:**
    ```sh
    python project.py
    ```

## Usage

- **Sign Up:** Enter your details and create a username and password.
- **Log In:** Use your credentials to access your dashboard.
- **Book Appointment:** Click "Book an Appointment", fill in the details, and select symptoms.
- **View Appointments:** See your appointments in a calendar view.
- **Edit/Delete:** Manage your appointments from the dashboard.
- **Settings:** Change your username or password.

## Data Files

- User and appointment data are stored in `data.json` and `appointments.json`.
- Symptoms and their severity are defined in `symptoms.json`.
- Postal code validation uses `postal_codes.csv`.

## Authors

- [@AP0tato](https://github.com/AP0tato)
- [@Felix3242](https://github.com/Felix3242)
- Aryan R.

## License

This project is for educational purposes.
