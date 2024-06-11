from PySide6 import QtWidgets, QtCore, QtGui
import re
import json
import csv

# Function to read data from a CSV file
def readFileCSV(file_name):
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile)
        return list(reader)

# Function to write user data to a JSON file
def writeFileJSON(data):
    with open('users.json', 'r+') as file:
        users = json.load(file)
        users.append(data)
        file.seek(0)
        json.dump(users, file, indent=4)

# Function to write appointment data to a JSON file
def writeFileJSON_Appointment(appointment, username):
    with open('appointments.json', 'r+') as file:
        appointments = json.load(file)
        if username in appointments:
            appointments[username].append(appointment)
        else:
            appointments[username] = [appointment]
        file.seek(0)
        json.dump(appointments, file, indent=4)

# Function to read appointment data from a JSON file
def readFileJSON_Appointment(username):
    with open('appointments.json', 'r') as file:
        appointments = json.load(file)
        return appointments.get(username, [])

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.setWindowTitle("Appointment Booking System")
        self.setGeometry(100, 100, 800, 600)

        # Initialize the log in page as the central widget
        self.central_widget = LogIn()
        self.setCentralWidget(self.central_widget)

class LogIn(QtWidgets.QFrame):
    """
    Initialize the log in page
    """
    def __init__(self):
        super().__init__()

        # Set the payout of the frame
        self.layout = QtWidgets.QGridLayout(self)

        # Different elements of the log in page
        self.error = QtWidgets.QLabel("Username or Password is incorrect")
        self.header = QtWidgets.QLabel("Log In", alignment=QtCore.Qt.AlignCenter)
        self.sign_up = QtWidgets.QPushButton("Sign Up")
        self.log_in = QtWidgets.QPushButton("Continue")
        self.username = QtWidgets.QLineEdit(placeholderText="Username")
        self.password = QtWidgets.QLineEdit(placeholderText="Password")
        self.error.setVisible(False)  # Hide error label initially

        # Add object names to all elements
        self.error.setObjectName("error")
        self.header.setObjectName("log_in")
        self.sign_up.setObjectName("log_in")
        self.log_in.setObjectName("log_in")
        self.username.setObjectName("log_in")
        self.password.setObjectName("log_in")

        # Add all of the elements to the log in page
        self.layout.addWidget(self.header, 2, 0)
        self.layout.addWidget(self.username, 0, 1)
        self.layout.addWidget(self.password, 1, 1)
        self.layout.addWidget(self.log_in, 2, 1)
        self.layout.addWidget(self.sign_up, 3, 1)

        # Make the two buttons do something
        self.sign_up.clicked.connect(self.signUp)
        self.log_in.clicked.connect(self.logIn)

    # Existing methods...

    """
    Shows the error message
    """
    def showError(self):
        self.error.setVisible(True)

    """
    Hides the error message
    """
    def hideError(self):
        self.error.setVisible(False)

    def logIn(self):
        # Hide the error message initially
        self.hideError()

        # Verify if the username is valid and that the password matches the username
        if not(self.verifyFields()):
            # Show the error message
            self.showError()
            return False
        
        # Verify if the username is valid and that the password matches the username
        if not(self.verifyFields()):
            self.layout.addWidget(self.error, 4, 1)
            return False
        
        for user in self.getData():
            if user.get("Username") == self.username.text():
                # Load all of the user data into the data variable
                data = user
        
        # Create the dashboard object using the user's data
        dashboard = DashBoard(data)
        # Destroy current window to prevent memory leaks
        self.destroy(destroySubWindows=True)
        # Change the displayed frame to the dashboard
        self.parent().setCentralWidget(dashboard)
        # Deletes the log in page to prevent memory leaks
        self.deleteLater()

    def signUp(self):
        sign_up = SignUp()
        self.destroy(destroySubWindows=True)
        self.parent().setCentralWidget(sign_up)
        self.deleteLater()

    def verifyFields(self):
        with open('users.json', 'r') as file:
            users = json.load(file)
            print("Loaded users:", users)  # Debugging print
            for user in users.get("users", []):
                print("User:", user)  # Debugging print
                if user.get("Username") == self.username.text() and user.get("Password") == self.password.text():
                    return True
        return False


    def getData(self):
        with open('users.json', 'r') as file:
            data = json.load(file)
            return data.get("users", [])

class SignUp(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self)

        self.header = QtWidgets.QLabel("Sign Up", alignment=QtCore.Qt.AlignCenter)
        self.first_name = QtWidgets.QLineEdit(placeholderText="First Name")
        self.last_name = QtWidgets.QLineEdit(placeholderText="Last Name")
        self.address = QtWidgets.QLineEdit(placeholderText="Address")
        self.postal_code = QtWidgets.QLineEdit(placeholderText="Postal Code")
        self.email_address = QtWidgets.QLineEdit(placeholderText="Email Address")
        self.phone_number = QtWidgets.QLineEdit(placeholderText="Phone Number")
        self.continue_button = QtWidgets.QPushButton("Continue")
        self.log_in = QtWidgets.QPushButton("Log In")
        self.error_label = QtWidgets.QLabel("1 or more fields are wrong.", alignment=QtCore.Qt.AlignCenter)

        self.header.setObjectName("header")
        self.error_label.setObjectName("error")
        self.first_name.setObjectName("sign_up")
        self.last_name.setObjectName("sign_up")
        self.address.setObjectName("sign_up")
        self.postal_code.setObjectName("sign_up")
        self.email_address.setObjectName("sign_up")
        self.phone_number.setObjectName("sign_up")
        self.continue_button.setObjectName("sign_up")
        self.log_in.setObjectName("sign_up")

        self.layout.addWidget(self.header)
        self.layout.addWidget(self.first_name)
        self.layout.addWidget(self.last_name)
        self.layout.addWidget(self.address)
        self.layout.addWidget(self.postal_code)
        self.layout.addWidget(self.email_address)
        self.layout.addWidget(self.phone_number)
        self.layout.addWidget(self.continue_button)
        self.layout.addWidget(self.log_in)

        self.continue_button.clicked.connect(self.continuSignUp)
        self.log_in.clicked.connect(self.logIn)

    def logIn(self):
        log_in = LogIn()
        self.destroy(destroySubWindows=True)
        self.parent().setCentralWidget(log_in)
        self.deleteLater()

    def continuSignUp(self):
        self.error_label.setParent(None)
        if self.verifyFields():
            sign_up = SignUp_Continuation(self.getData())
            self.destroy(destroySubWindows=True)
            self.parent().setCentralWidget(sign_up)
            self.deleteLater()
        else:
            self.layout.addWidget(self.error_label)

    def verifyFields(self):
        if any(not field.text() for field in [self.first_name, self.last_name, self.address, self.postal_code, self.email_address, self.phone_number]):
            return False
        if not self.verifyPostalCode(self.postal_code.text()):
            return False
        if not self.verifyEmail(self.email_address.text()):
            return False
        if not self.verifyPhoneNumber(self.phone_number.text()):
            return False
        return True

    def verifyPostalCode(self, postal_code):
        postal_codes = readFileCSV("postal_codes.csv")
        return any(postal_code in row for row in postal_codes)

    def verifyEmail(self, email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(pattern, email))

    def verifyPhoneNumber(self, phone_number):
        pattern = r'^\+?\d{10,15}$'
        return bool(re.match(pattern, phone_number))

    def getData(self):
        return {
            "First Name": self.first_name.text(),
            "Last Name": self.last_name.text(),
            "Address": self.address.text(),
            "Postal Code": self.postal_code.text(),
            "Email Address": self.email_address.text(),
            "Phone Number": self.phone_number.text()
        }

class SignUp_Continuation(QtWidgets.QFrame):
    def __init__(self, data):
        super().__init__()

        self.data = data

        self.layout = QtWidgets.QVBoxLayout(self)

        self.header = QtWidgets.QLabel("Complete Your Sign Up", alignment=QtCore.Qt.AlignCenter)
        self.log_in = QtWidgets.QPushButton("Log In")
        self.sign_up = QtWidgets.QPushButton("Sign Up")
        self.username = QtWidgets.QLineEdit(placeholderText="Username")
        self.password = QtWidgets.QLineEdit(placeholderText="Password")
        self.confirm_password = QtWidgets.QLineEdit(placeholderText="Confirm Password")
        self.error_label = QtWidgets.QLabel("1 or more fields are wrong.", alignment=QtCore.Qt.AlignCenter)

        self.header.setObjectName("header")
        self.error_label.setObjectName("error")
        self.log_in.setObjectName("sign_up")
        self.sign_up.setObjectName("sign_up")
        self.username.setObjectName("sign_up")
        self.password.setObjectName("sign_up")
        self.confirm_password.setObjectName("sign_up")

        self.layout.addWidget(self.header)
        self.layout.addWidget(self.username)
        self.layout.addWidget(self.password)
        self.layout.addWidget(self.confirm_password)
        self.layout.addWidget(self.sign_up)
        self.layout.addWidget(self.log_in)

        self.sign_up.clicked.connect(self.completeSignUp)
        self.log_in.clicked.connect(self.logIn)

    def logIn(self):
        log_in = LogIn()
        self.destroy(destroySubWindows=True)
        self.parent().setCentralWidget(log_in)
        self.deleteLater()

    def completeSignUp(self):
        self.error_label.setParent(None)
        if self.verifyFields():
            user_data = self.data
            user_data["Username"] = self.username.text()
            user_data["Password"] = self.password.text()
            writeFileJSON(user_data)
            log_in = LogIn()
            self.destroy(destroySubWindows=True)
            self.parent().setCentralWidget(log_in)
            self.deleteLater()
        else:
            self.layout.addWidget(self.error_label)

    def verifyFields(self):
        if any(not field.text() for field in [self.username, self.password, self.confirm_password]):
            return False
        if self.password.text() != self.confirm_password.text():
            return False
        if not self.verifyUsername(self.username.text()):
            return False
        return True

    def verifyUsername(self, username):
        with open('users.json', 'r') as file:
            users = json.load(file)
            return all(user["Username"] != username for user in users)

class DashBoard(QtWidgets.QFrame):
    def __init__(self, data):
        super().__init__()

        self.data = data

        self.layout = QtWidgets.QVBoxLayout(self)

        self.header = QtWidgets.QLabel(f"Welcome, {self.data['First Name']} {self.data['Last Name']}!", alignment=QtCore.Qt.AlignCenter)
        self.book_appointment = QtWidgets.QPushButton("Book an Appointment")
        self.view_appointments = QtWidgets.QPushButton("View Appointments")
        self.log_out = QtWidgets.QPushButton("Log Out")

        self.header.setObjectName("dashboard")
        self.book_appointment.setObjectName("dashboard")
        self.view_appointments.setObjectName("dashboard")
        self.log_out.setObjectName("dashboard")

        self.layout.addWidget(self.header)
        self.layout.addWidget(self.book_appointment)
        self.layout.addWidget(self.view_appointments)
        self.layout.addWidget(self.log_out)

        self.book_appointment.clicked.connect(self.bookAppointment)
        self.view_appointments.clicked.connect(self.viewAppointments)
        self.log_out.clicked.connect(self.logOut)

    def bookAppointment(self):
        book_appointment = BookAppointment(self.data)
        self.destroy(destroySubWindows=True)
        self.parent().setCentralWidget(book_appointment)
        self.deleteLater()

    def viewAppointments(self):
        view_appointments = ViewAppointments(self.data)
        self.destroy(destroySubWindows=True)
        self.parent().setCentralWidget(view_appointments)
        self.deleteLater()

    def logOut(self):
        log_in = LogIn()
        self.destroy(destroySubWindows=True)
        self.parent().setCentralWidget(log_in)
        self.deleteLater()

class BookAppointment(QtWidgets.QFrame):
    def __init__(self, data):
        super().__init__()

        self.data = data

        self.layout = QtWidgets.QVBoxLayout(self)

        self.header = QtWidgets.QLabel("Book an Appointment", alignment=QtCore.Qt.AlignCenter)
        self.back = QtWidgets.QPushButton("Back")
        self.date = QtWidgets.QLineEdit(placeholderText="Date (YYYY-MM-DD)")
        self.time = QtWidgets.QLineEdit(placeholderText="Time (HH:MM)")
        self.reason = QtWidgets.QLineEdit(placeholderText="Reason for Appointment")
        self.book = QtWidgets.QPushButton("Book Appointment")
        self.error_label = QtWidgets.QLabel("1 or more fields are wrong.", alignment=QtCore.Qt.AlignCenter)

        self.header.setObjectName("book_appointment")
        self.error_label.setObjectName("error")
        self.back.setObjectName("book_appointment")
        self.date.setObjectName("book_appointment")
        self.time.setObjectName("book_appointment")
        self.reason.setObjectName("book_appointment")
        self.book.setObjectName("book_appointment")

        self.layout.addWidget(self.header)
        self.layout.addWidget(self.date)
        self.layout.addWidget(self.time)
        self.layout.addWidget(self.reason)
        self.layout.addWidget(self.book)
        self.layout.addWidget(self.back)

        self.book.clicked.connect(self.bookAppointment)
        self.back.clicked.connect(self.goBack)

    def goBack(self):
        dashboard = DashBoard(self.data)
        self.destroy(destroySubWindows=True)
        self.parent().setCentralWidget(dashboard)
        self.deleteLater()

    def bookAppointment(self):
        self.error_label.setParent(None)
        if self.verifyFields():
            appointment = {
                "Date": self.date.text(),
                "Time": self.time.text(),
                "Reason": self.reason.text()
            }
            writeFileJSON_Appointment(appointment, self.data["Username"])
            dashboard = DashBoard(self.data)
            self.destroy(destroySubWindows=True)
            self.parent().setCentralWidget(dashboard)
            self.deleteLater()
        else:
            self.layout.addWidget(self.error_label)

    def verifyFields(self):
        if any(not field.text() for field in [self.date, self.time, self.reason]):
            return False
        if not self.verifyDate(self.date.text()):
            return False
        if not self.verifyTime(self.time.text()):
            return False
        return True

    def verifyDate(self, date):
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        return bool(re.match(pattern, date))

    def verifyTime(self, time):
        pattern = r'^\d{2}:\d{2}$'
        return bool(re.match(pattern, time))

class ViewAppointments(QtWidgets.QFrame):
    def __init__(self, data):
        super().__init__()

        self.data = data

        self.layout = QtWidgets.QVBoxLayout(self)

        self.header = QtWidgets.QLabel("Your Appointments", alignment=QtCore.Qt.AlignCenter)
        self.back = QtWidgets.QPushButton("Back")
        self.appointments = QtWidgets.QListWidget()
        self.delete_appointment = QtWidgets.QPushButton("Delete Appointment")

        self.header.setObjectName("view_appointments")
        self.back.setObjectName("view_appointments")
        self.appointments.setObjectName("view_appointments")
        self.delete_appointment.setObjectName("view_appointments")

        self.layout.addWidget(self.header)
        self.layout.addWidget(self.appointments)
        self.layout.addWidget(self.delete_appointment)
        self.layout.addWidget(self.back)

        self.loadAppointments()

        self.back.clicked.connect(self.goBack)
        self.delete_appointment.clicked.connect(self.deleteAppointment)

    def goBack(self):
        dashboard = DashBoard(self.data)
        self.destroy(destroySubWindows=True)
        self.parent().setCentralWidget(dashboard)
        self.deleteLater()

    def loadAppointments(self):
        appointments = readFileJSON_Appointment(self.data["Username"])
        for appointment in appointments:
            item = QtWidgets.QListWidgetItem(f"Date: {appointment['Date']}, Time: {appointment['Time']}, Reason: {appointment['Reason']}")
            self.appointments.addItem(item)

    def deleteAppointment(self):
        selected_item = self.appointments.currentItem()
        if selected_item:
            self.appointments.takeItem(self.appointments.row(selected_item))
            appointments = readFileJSON_Appointment(self.data["Username"])
            for appointment in appointments:
                if f"Date: {appointment['Date']}, Time: {appointment['Time']}, Reason: {appointment['Reason']}" == selected_item.text():
                    appointments.remove(appointment)
                    break
            writeFileJSON_Appointment(appointments, self.data["Username"])

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    main_window = MainWindow()
    main_window.show()

    app.exec_()
