import sys
import json
import csv
import re
from datetime import datetime, timedelta, date
from calendar import monthrange
from PySide6 import QtCore, QtWidgets

"""
Read qss file
"""
def readQSS(file: str):
    with open(file, 'r') as f:
        return f.read()

"""
Deletes an appointment from JSON file
"""
def deleteApointmentJSON(appointment: list, username: str):
    appointments = readFileJSON("appointments.json")
    appointments[username].remove(appointment)
    with open("appointments.json", "w+") as file:
        file.write("{\n}")
        file.seek(0)
        json.dump(appointments, file, indent=4)

"""
Function to write appointment data to a JSON file
"""
def writeFileJSON_Appointment(appointment: list, username: str):
    with open('appointments.json', 'r+') as file:
        appointments = json.load(file)
        if username in appointments:
            appointments[username] = appointment
        else:
            appointments[username] = [appointment]
        file.seek(0)
        json.dump(appointments, file, indent=4)

"""
Function to read appointment data from a JSON file
"""
def readFileJSON_Appointment(username: str):
    with open('appointments.json', 'r') as file:
        appointments = json.load(file)
        return appointments.get(username)

"""
Read any JSON file with a given file path (Optional)
"""
def readFileJSON(file = "data.json"):
    try:
        # Open the file and load the data into a variable, then return the data
        with open(file, 'r') as f:
            data = json.load(f)
        return data
    # Exception for file not found and incorrect JSON format
    except FileNotFoundError:
        print(f"Error: The file {file} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file {file} contains invalid JSON.")
        return None

"""
Writes data to a given JSON file
"""
def writeFileJSON(data: dict, file = "data.json"):
    # Get all the previous data and load it
    d = readFileJSON(file)
    # Add the new data
    d["users"].append(data)
    # Write the data to the given JSON file
    with open(file, 'w', encoding='utf-8') as f:
        obj = json.dumps(d, ensure_ascii=False, indent=4)
        f.write(obj)

"""
The main window of the program; all widgets will be displayed on this window
"""
class Window(QtWidgets.QMainWindow):
    """
    Initialize the main window
    """
    def __init__(self):
        super().__init__()
        # Styling the pages
        self.setStyleSheet(readQSS("main.qss"))
        # Set window title
        self.setWindowTitle("HABS")
        # Set window size
        self.setGeometry(0, 0, 800, 400)
        # Load the first page of the program - the log in page
        log_in = LogIn()
        # Set the log in page as the main frame/widget
        self.setCentralWidget(log_in)

"""
The log in page of the program
"""
class LogIn(QtWidgets.QFrame):
    """
    Initialize the log in page
    """
    def __init__(self):
        super().__init__()

        # Set the payout of the frame
        self.layout = QtWidgets.QVBoxLayout(self)

        # Different elements of the log in page
        self.error = QtWidgets.QLabel("Username or Password is incorrect")
        self.header = QtWidgets.QLabel("Log In", alignment=QtCore.Qt.AlignCenter)
        self.sign_up = QtWidgets.QPushButton("Sign Up")
        self.log_in = QtWidgets.QPushButton("Continue")
        self.username = QtWidgets.QLineEdit(placeholderText = "Username")
        self.password = QtWidgets.QLineEdit(placeholderText = "Password")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        # Add all of the elements to the log in page
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.username)
        self.layout.addWidget(self.password)
        self.layout.addWidget(self.log_in)
        self.layout.addWidget(self.sign_up)

        # Make the two buttons do something
        self.sign_up.clicked.connect(self.signUp)
        self.log_in.clicked.connect(self.logIn)

    """
    Changes the current page to the sign up page
    """
    def signUp(self):
        # Create the sign up page object
        sign_up = SignUp()
        # Destroy current window to prevent memory leaks
        self.destroy(destroySubWindows=True)
        # Change the displayed frame to the sign up page
        self.parent().setCentralWidget(sign_up)
        # Deletes the log in page to prevent memory leaks
        self.deleteLater()
    
    """
    Changes the current page to the dashboard of the user
    """
    def logIn(self):
        # Reset the error message if it was previously displayed
        self.error.setParent(None)
        # Verify if the username if valid and that the password matches the username
        if not(self.verifyUsername() and self.verifyPassword()):
            self.layout.addWidget(self.error)
            return False
        d = readFileJSON()
        for i in d["users"]:
            if i.get("Username")==self.username.text():
                # Load all of the user data into the data variable
                data = i
        # Create the dashboard object using the users data
        dashboard = DashBoard(data)
        # Destroy current window to prevent memory leaks
        self.destroy(destroySubWindows=True)
        # Change the displayed frame to the dashboard
        self.parent().setCentralWidget(dashboard)
        # Deletes the log in page to prevent memory leaks
        self.deleteLater()

    """
    Checks if the username is valid
    """
    def verifyUsername(self):
        # Get inputed username
        txt = self.username.text()
        d = readFileJSON()
        # Make sure loaded data is in correct format
        if isinstance(d, dict) and "users" in d:
            for user in d["users"]:
                # Check if that username exists
                if user.get("Username") == txt:
                    # It exists
                    return True
        # It does not exist
        return False
    
    """
    Checks if the password matches the usernames password
    """
    def verifyPassword(self):
        # Get the inputted password
        txt = self.password.text()
        d = readFileJSON()
        # Make sure loaded data is in correct format
        if isinstance(d, dict) and "users" in d:
            for i in d["users"]:
                # Find the user data that corresponds to the username given
                if i.get("Username")==self.username.text():
                    # Check if the password matches the users password
                    return txt==i.get("Password")

"""
The sign up page for the program
"""
class SignUp(QtWidgets.QFrame):
    """
    Initialize the sign up page
    """
    def __init__(self):
        super().__init__()

        # Set the layout of the frame
        self.layout = QtWidgets.QVBoxLayout(self)

        # Create all the elements that is needed for the sign up page
        self.header = QtWidgets.QLabel("Sign Up", alignment=QtCore.Qt.AlignCenter)
        self.log_in = QtWidgets.QPushButton("Log In")
        self.continu = QtWidgets.QPushButton("Continue")
        self.first_name = QtWidgets.QLineEdit(placeholderText = "First Name")
        self.last_name = QtWidgets.QLineEdit(placeholderText = "Last Name")
        self.address = QtWidgets.QLineEdit(placeholderText = "Address (Number Road)")
        self.postal_code = QtWidgets.QLineEdit(placeholderText = "Postal Code")
        self.email_address = QtWidgets.QLineEdit(placeholderText = "Email Address")
        self.phone_number = QtWidgets.QLineEdit(placeholderText = "Phone Number")
        self.error_label = QtWidgets.QLabel("1 or more fields are wrong.", alignment=QtCore.Qt.AlignCenter)

        # Add all the elements to the sign up page
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.first_name)
        self.layout.addWidget(self.last_name)
        self.layout.addWidget(self.address)
        self.layout.addWidget(self.postal_code)
        self.layout.addWidget(self.email_address)
        self.layout.addWidget(self.phone_number)
        self.layout.addWidget(self.continu)
        self.layout.addWidget(self.log_in)

        # Makes buttons do stuff
        self.continu.clicked.connect(self.continuFunc)
        self.log_in.clicked.connect(self.logIn)

    """
    Change the page to the log in page
    """
    def logIn(self):
        # Create the log in object
        log_in = LogIn()
        # Destroy current fram
        self.destroy(destroySubWindows=True)
        # Set the log in page as the main page
        self.parent().setCentralWidget(log_in)
        # Delete the current page to prevent memory leaks
        self.deleteLater()

    """
    Change the page to the next sign up page
    """
    def continuFunc(self):
        # Reset the error label
        self.error_label.setText("")
        self.error_label.setParent(None)
        # Get all the inputed information into a variables
        self.data = {"First Name": self.first_name.text(), "Last Name": self.last_name.text(), "Email Address": self.email_address.text(), 
                "Phone Number": self.phone_number.text(), "Address": self.address.text(), "Postal Code": self.postal_code.text()}
        # A bunch of checks to see if the input in the fields are valid, each giving different error messages if they're not
        if not self.verifyEmail():
            self.error_label.setText(self.error_label.text()+"Email is not valid. ")
            self.layout.addWidget(self.error_label)
        if not self.verifyPhoneNumber():
            self.error_label.setText(self.error_label.text()+"Phone number is not valid. ")
            self.layout.addWidget(self.error_label)
        if not self.verifyPostalCode():
            self.error_label.setText(self.error_label.text()+"Postal code is not valid. ")
            self.layout.addWidget(self.error_label)
        if not self.verifyName():
            self.error_label.setText(self.error_label.text()+"Name cannot be blank or have numbers. ")
            self.layout.addWidget(self.error_label)
        # Exit the function and do nothing if one the checks fail
        if not(self.verifyEmail() and self.verifyName() and self.verifyPhoneNumber() and self.verifyPostalCode()):
            return False
        # Create the next sign up page
        sign_up = SignUp1(self.data)
        # Destroy current frame
        self.destroy(destroySubWindows=True)
        # Set the new main page to the next sign up page
        self.parent().setCentralWidget(sign_up)
        # Delete the current page to prevent memory leaks
        self.deleteLater()

    """
    Makes sure that the given name is valid (No numbers or symbols)
    """
    def verifyName(self):
        # Get the given first and last name
        txt_first = self.first_name.text()
        txt_last = self.first_name.text()
        # Check if they are valid
        return re.search(r"\w", txt_first) and re.search(r"\w", txt_last)

    """
    Makes sure that the email given is real (Matches certain requirements)
    """
    def verifyEmail(self):
        # Get the given emails
        txt = self.email_address.text()
        # Check if the email is valid
        return re.search(r"^.+@(.+\..+)+(|\..+)$", txt)
    
    """
    Makes sure the phone number is valid (10 digits long)
    """
    def verifyPhoneNumber(self):
        # Get the given phone number
        txt = self.phone_number.text()
        # Get only the digits of the phone number
        txt = re.sub(r'\D', "", txt)
        # Check if the phone number is valid
        return len(txt)==10
    
    """
    Make sure that the first 3 symbols the postal code are valid
    """
    def verifyPostalCode(self):
        pCode = self.postal_code.text().upper().replace(" ", "")
        if(len(pCode)!=6):
            return False
        # Open the file
        with open("postal_codes.csv", encoding="windows-1252") as file:
            csvReader = csv.reader(file, delimiter="|")
            for row in csvReader:
                # Check the first 3 digits of the given postal code and see if there are matches
                if row[0]==pCode[:3]:
                    # Return valid postal code
                    file.close()
                    return True
            # The postal code is not valid
            file.close()
            return False

"""
The next sign up page
"""
class SignUp1(SignUp):
    """
    Initialize the seconds sign up page
    """
    def __init__(self, data: dict):
        super().__init__()

        # Remove all previously displayed things (It inherits form SignUp, that's why)
        self.address.setParent(None)
        self.postal_code.setParent(None)
        self.first_name.setParent(None)
        self.last_name.setParent(None)
        self.continu.setParent(None)
        self.log_in.setParent(None)
        self.email_address.setParent(None)
        self.phone_number.setParent(None)

        # Create all the variales and elements
        self.data = data
        self.username = QtWidgets.QLineEdit(placeholderText = "Username")
        self.password = QtWidgets.QLineEdit(placeholderText = "Password (8 characters, 1 number, 1 upper case, 1 special character)")
        self.continu = QtWidgets.QPushButton("Continue")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

        # Add all the elements to the frame
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.username)
        self.layout.addWidget(self.password)
        self.layout.addWidget(self.continu)
        self.layout.addWidget(self.cancel_btn)

        # Make the button do something
        self.continu.clicked.connect(self.continuFunc)
        self.cancel_btn.clicked.connect(self.cancel)
    
    """
    Cancel the sign up process and bring the user back to the log in page
    """
    def cancel(self):
        log_in = LogIn()
        self.destroy(destroySubWindows=True)
        self.parent().setCentralWidget(log_in)
        self.deleteLater()

    """
    Go to the users dashboard
    """
    def continuFunc(self):
        # Reset any error labels
        self.error_label.setParent(None)
        # Store the given username and password
        self.data["Username"] = self.username.text()
        self.data["Password"] = self.password.text()
        # Verify the username and the password
        if not self.verifyUsername():
            self.error_label.setText("Username is not valid")
            self.layout.addWidget(self.error_label)
            return False
        elif not self.verifyPassword():
            self.error_label.setText("Password is not valid")
            self.layout.addWidget(self.error_label)
            return False
        # Save the data
        writeFileJSON(self.data)
        # Create the log in object
        log_in = LogIn()
        # Destroy current window
        self.destroy(destroySubWindows=True)
        # Set current window to the log in page
        self.parent().setCentralWidget(log_in)
        # Delete current page to prevent memory leaks
        self.deleteLater()
    
    """
    Verify the username
    """
    def verifyUsername(self):
        # Get the given username
        txt = self.username.text()
        # Get the old data and check if that username already exists
        d = readFileJSON()
        for i in d:
            try:
                if i["Username"]==txt:
                    # It exsists; invalid
                    return False
            except:
                pass
        # Check if the username doesn't contain any special charatcers that can cause problems
        return re.search(r"[^\\/?\"\'\:;\+\*\&\^\(\)\=\[\]\{\}\<\>\-]", txt)
    
    """
    Verify the password
    """
    def verifyPassword(self):
        # Get the given password
        txt = self.password.text()
        # Verify the pass word - 8 characters long, 1 special character, 1 uppercase letter and 1 digit (Minimum)
        return re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", txt) and len(txt)>=8

"""
The users dashboard
"""
class DashBoard(QtWidgets.QFrame):
    """
    Initialize the user's dashboard
    """
    def __init__(self, data: dict):
        super().__init__()

        # Set the layout of the frame
        self.layout = QtWidgets.QVBoxLayout(self)

        # Create all elements and variables
        self.data = data
        self.header = QtWidgets.QLabel(f"Welcome, {self.data.get("First Name")} {self.data.get("Last Name")}!", alignment=QtCore.Qt.AlignCenter)
        self.user_calender = QtWidgets.QPushButton("View Appointments")
        self.user_bookings = QtWidgets.QPushButton("Book an Appointment")
        self.log_out = QtWidgets.QPushButton("Log Out")
        self.settings = QtWidgets.QPushButton("Settings")

        # Add all the elements to the main page
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.user_bookings)
        self.layout.addWidget(self.user_calender)
        self.layout.addWidget(self.settings)
        self.layout.addWidget(self.log_out)

        # Make the buttons do something
        self.user_bookings.clicked.connect(self.bookings)
        self.user_calender.clicked.connect(self.viewAppointments)
        self.log_out.clicked.connect(self.logOut)
        self.settings.clicked.connect(self.setting)

    """
    Go to the user's settings page
    """
    def setting(self):
        # Create the settings object
        settings = Settings(self.data)
        # Destroy current window
        self.destroy(destroySubWindows=True)
        # Change the main window to the settings window
        self.parent().setCentralWidget(settings)
        # Destroy this object to prevent memory leaks
        self.deleteLater()

    """
    The log out function
    """
    def logOut(self):
        # The log in object
        log_in = LogIn()
        # Destroy current window
        self.destroy(destroySubWindows=True)
        # Change current window to the log in page
        self.parent().setCentralWidget(log_in)
        # Delete the current page to prevent memory leaks
        self.deleteLater()

    """
    The booking page for the user
    """
    def bookings(self):
        # Create the booking page object with the user data
        bookings = Booking(self.data)
        # Destroy the current window
        self.destroy(destroySubWindows=True)
        # Change the main window to the booking window
        self.parent().setCentralWidget(bookings)
        # Delete the current object to prevent memory leaks
        self.deleteLater()

    """
    The calendar of the user
    """
    def viewAppointments(self):
        # Create the view appointments object
        view_appointments = ViewAppointments(self.data)
        # Destroy current frame
        self.destroy(destroySubWindows=True)
        # Change main frame to apointment view
        self.parent().setCentralWidget(view_appointments)
        # Delete object to prevent memory leaks
        self.deleteLater()

"""
A widget to display a month
"""
class Month(QtWidgets.QWidget):
    """
    Initialize the month given
    """
    def __init__(self, date: str, data: dict):
        super().__init__()

        # Set the layout of the widget
        self.layout = QtWidgets.QGridLayout(self)

        # All variables and elements
        self.data = data
        self.month_names = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 
                       8:" August", 9: "September", 10: "October", 11: "November", 12: "December"}
        self.day_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

        self.days_in_month = 0
        self.header = QtWidgets.QLabel("")
        self.date = date.strip().split("-")
        self.month = self.date[1]
        self.year = self.date[0]

        self.days_in_month = monthrange(int(self.year), int(self.month))

        self.header.setText(f'{self.month_names.get(int(self.month))} {self.year}')
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.left_btn = QtWidgets.QPushButton("<")
        self.right_btn = QtWidgets.QPushButton(">")
        self.back_btn = QtWidgets.QPushButton("Back")

        # Add all the elements to the calender page
        self.layout.addWidget(self.left_btn, 0, 0)
        self.layout.addWidget(self.right_btn, 0, 6)
        self.layout.addWidget(self.header, 0, 3)
        for i in range(7):
            self.layout.addWidget(QtWidgets.QLabel(self.day_names[i], alignment=QtCore.Qt.AlignCenter), 1, i)

        # Make the buttons do something
        self.left_btn.clicked.connect(self.left)
        self.right_btn.clicked.connect(self.right)
        self.back_btn.clicked.connect(self.back)

        # Set current row
        row = 2
        for i in range(1, self.days_in_month[1]+1):
            # Format the current day the loop is on
            str = f'{self.year}-{self.month}-{i}'
            # Create the day object
            day = Day(str, i, self.data)
            # Previous day
            pre_str = datetime(int(self.year), int(self.month), i).weekday()
            # Check if the previous day was saturday
            if pre_str==6:
                # Move on to the next row
                row += 1
            # Add the day object to the frame
            self.layout.addWidget(day, row, (day.day+1)%7)
        self.layout.addWidget(self.back_btn, row+1, 3)

    """
    Move to the next month
    """
    def right(self):
        # Check if the month is december
        if int(self.month)==12:
            # Increase the year and set the month to january
            self.year = int(self.year)+1
            self.month = 1
        else:
            # Increase the month by 1
            self.month = int(self.month)+1
        # Format the month and the year and call the Month object using the string
        next = Month(f'{self.year}-{self.month}', self.data)
        # Change the main frame to the next month
        self.parent().setCentralWidget(next)
        # Destroy current frame
        self.destroy(destroySubWindows=True)
        # Delete current object to prevent memory leaks
        self.deleteLater()

    """
    Move to the previous month
    """
    def left(self):
        # Check if the month is january
        if int(self.month)==1:
            # Decrease the year by 1 and set the month to december
            self.year = int(self.year)-1
            self.month = 12
        else:
            # Decreaste the month by 1
            self.month = int(self.month)-1
        # Format the month and the year and call the Month object using the string
        back = Month(f'{self.year}-{self.month}', self.data)
        # Set the current frame to the previous month
        self.parent().setCentralWidget(back)
        # Destroy current window
        self.destroy(destroySubWindows=True)
        # Delete object to prevent memory leaks
        self.deleteLater()
    
    """
    Go to the user's dashboard
    """
    def back(self):
        appointments = ViewAppointments(self.data)
        # Set the current frame to the previous month
        self.parent().setCentralWidget(appointments)
        # Destroy current window
        self.destroy(destroySubWindows=True)
        # Delete object to prevent memory leaks
        self.deleteLater()

"""
The day object
"""
class Day(QtWidgets.QWidget):
    """
    Initialize a day using user data
    """
    def __init__(self, date: str, day_num: int, data: dict):
        super().__init__()

        # Set the layout of the widget
        self.layout = QtWidgets.QVBoxLayout(self)

        # All variables and elements
        self.date = ""
        self.day_names = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
        self.data = data
        self.date = date.strip().split("-")
        self.day_num = day_num
        self.day = datetime(int(self.date[0]), int(self.date[1]), self.day_num).weekday()
        self.label = QtWidgets.QLabel(str(self.day_num), alignment=QtCore.Qt.AlignCenter)
        self.appointments = readFileJSON_Appointment(self.data["Username"])

        # Add elements to the day widget
        self.layout.addWidget(self.label)

        for i in self.appointments:
            temp = datetime(int(self.date[0]), int(self.date[1]), self.day_num).strftime("%Y-%m-%d")
            if temp==i["Date"]:
                self.label.setStyleSheet("background-color: green;")

"""
The booking page for the user
"""
class Booking(QtWidgets.QFrame):
    """
    Initialize the object
    """
    def __init__(self, data: dict):
        super().__init__()

        # Set the layout
        self.layout = QtWidgets.QVBoxLayout(self)

        # All variables and elements
        self.data = data
        self.symptoms_selected = []
        self.header = QtWidgets.QLabel("Book an Appointment", alignment=QtCore.Qt.AlignCenter)
        self.back = QtWidgets.QPushButton("Back")
        self.date = QtWidgets.QLineEdit(placeholderText="Prefered Date (YYYY-MM-DD)")
        self.time = QtWidgets.QLineEdit(placeholderText="Prefered Time 24h (HH:MM)")
        self.reason = QtWidgets.QPushButton("Reasons for Appointment")
        self.book = QtWidgets.QPushButton("Book Appointment")
        self.error_label = QtWidgets.QLabel("1 or more fields are wrong.", alignment=QtCore.Qt.AlignCenter)

        # Add them to the frame
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.date)
        self.layout.addWidget(self.time)
        self.layout.addWidget(self.reason)
        self.layout.addWidget(self.book)
        self.layout.addWidget(self.back)

        # Make the buttons do stuff
        self.book.clicked.connect(self.bookAppointment)
        self.back.clicked.connect(self.goBack)
        self.reason.clicked.connect(self.viewSymptoms)

    """
    Open the symptom select page
    """
    def viewSymptoms(self):
        symptoms = Symptoms(self.data, [self.date.text(), self.time.text()], self.symptoms_selected)
        self.destroy(destroySubWindows=True)
        self.parent().setCentralWidget(symptoms)
        self.deleteLater()

    """
    Go to use dashboard
    """
    def goBack(self):
        # Create dashboard object
        dashboard = DashBoard(self.data)
        # Destroy current frame
        self.destroy(destroySubWindows=True)
        # Change main frame to user dashboard
        self.parent().setCentralWidget(dashboard)
        # Delete object to prevent memory leaks
        self.deleteLater()

    """
    Book an appointment
    """
    def bookAppointment(self):
        # Reset error label
        self.error_label.setParent(None)
        # Check if the fields' input are valid
        reasons = []
        for i in self.symptoms_selected:
            if i:
                reasons.append(i)
        if self.verifyFields():
            appointment = {
                "Date": self.date.text(),
                "Time": self.time.text(),
                "Reasons": reasons
            }
            sorted_appointments = self.sortAppointment(appointment, self.data["Username"])
            # Write to the appointment file
            writeFileJSON_Appointment(sorted_appointments, self.data["Username"])
            # Create the dashboard object
            dashboard = DashBoard(self.data)
            # Destroy current frame
            self.destroy(destroySubWindows=True)
            # Set dashboard as main frame
            self.parent().setCentralWidget(dashboard)
            # Destory object to prevent memory leaks
            self.deleteLater()
        else:
            # Error message
            self.layout.addWidget(self.error_label)

    """
    Check if the fields are completed
    """
    def verifyFields(self):
        if any(not field.text() for field in [self.date, self.time]):
            return False
        if not self.symptoms_selected:
            return False
        if not self.verifyDate(self.date.text()):
            return False
        if not self.verifyTime(self.time.text()):
            return False
        # They are all completed
        return True

    """
    Check and see if a given date is in the valid formt and if the day is in the past
    """
    def verifyDate(self, date: str):
        # Check if date is in the past
        date = date.strip()
        year, month, day = int(date.split("-")[0]), int(date.split("-")[1]), int(date.split("-")[2])
        if year <= datetime.today().year:
            if month <= datetime.today().month:
                if day < datetime.today().day: 
                    return False
                
        # Check if the numbers are valid
        try:
            t = datetime(year, month, day)
        except:
            return False
        
        # Check if formatted correctly
        pattern = r'^\d{4}-\d{1,2}-\d{1,2}$'
        return bool(re.match(pattern, date))

    """
    Check if the time is in the correct format
    """
    def verifyTime(self, time: str):
        pattern = r'^[012]*\d{1}:\d{2}$'
        return bool(re.match(pattern, time))
    
    """
    Change appointment time based on symptom severity
    """
    def sortAppointment(self, appointment: dict, username: str):
        # Get severity of appointment
        severity = self.getSeverity(appointment)
        # Get all other appointments that the user has
        appointments = readFileJSON_Appointment(username)
        new_appointment_date = ""

        # Get current and appoitnment date and format it
        current_date = datetime.today().strftime("%Y-%m-%d")
        current_date = datetime.strptime(current_date, "%Y-%m-%d")
        appointment_date = datetime.strptime(appointment["Date"], "%Y-%m-%d")
        # Find the days between the two
        day_difference = abs((appointment_date - current_date).days)

        # Decide whether to reschedual the appointment
        if day_difference+(severity*2)>20:
            day_difference -= (11-severity)
            temp = appointment["Date"].split("-")
            new_appointment_date = date(int(temp[0]), int(temp[1]), int(temp[2])) - timedelta(days=day_difference)  
        else:
            new_appointment_date = appointment_date

        # Do any changes needed
        appointment["Date"] = new_appointment_date.strftime("%Y-%m-%d")
        appointments = self.mergeAppointments(appointment, username)

        return appointments

    """
    Merge two appointments with the same date
    """
    def mergeAppointments(self, appointment: dict, username: str):
        appointments = readFileJSON_Appointment(username)
        merged = False
        if not appointments:
            appointments = appointment
            return appointments
        for i in range(len(appointments)):
            # Check if the two appointments are the same
            if appointment["Date"]==appointments[i]["Date"]:
                # Merge the reasons together
                appointments[i]["Reasons"] = list(set(appointments[i]["Reasons"]+appointment["Reasons"]))
                merged = True
                break
        if not merged:
            appointments.append(appointment)
        return appointments
    
    """
    Get the severity of the appointment
    """
    def getSeverity(self, appointment: dict):
        symptom_severity = readFileJSON("symptoms.json")
        highest_severity = 0
        # Go through all the reasons the user has listed, and if the severity associated 
        # with the symptom is higher than the current highest, change the sevrity
        for i in appointment["Reasons"]:
            for j in symptom_severity:
                for k in symptom_severity[j]:
                    temp = k[list(k.keys())[0]] if list(k.keys())[0]==i else 0
                    highest_severity = temp if temp>highest_severity else highest_severity
        return highest_severity

"""
Gives the user the option to select from a list of symptoms
"""
class Symptoms(QtWidgets.QFrame):
    def __init__(self, data: dict, parent_data: list, symptoms_selected: list):
        super().__init__()

        # Set the layout of the frame
        self.layout = QtWidgets.QVBoxLayout(self)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)

        self.central_widget = QtWidgets.QWidget()
        self.qvbox = QtWidgets.QVBoxLayout()

        # Prepare all the ckeckboxes
        self.symptom_list = readFileJSON("symptoms.json")
        self.data = data
        self.parent_data = parent_data
        self.checkbox_list = []
        for i in self.symptom_list:
            temp = []
            for j in self.symptom_list[i]:
                temp.append(QtWidgets.QCheckBox(list(j.keys())[0].capitalize()))
            self.checkbox_list.append({QtWidgets.QLabel(i.upper()): temp})
        self.back_btn = QtWidgets.QPushButton("Back")

        # Get previous user inputs
        if symptoms_selected:
            for i in symptoms_selected:
                for j in self.checkbox_list:
                    for k in j[list(j.keys())[0]]:
                        try:
                            if i==k.text().lower():
                                k.setChecked(True)
                                break
                        except:
                            pass

        # Add all checkboxes to the main frame
        for i in self.checkbox_list:
            self.qvbox.addWidget(list(i.keys())[0])
            for j in i[list(i.keys())[0]]:
                self.qvbox.addWidget(j)

        self.central_widget.setLayout(self.qvbox)
        self.scroll_area.setWidget(self.central_widget)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.back_btn)

        # Make button do stuff
        self.back_btn.clicked.connect(self.back)

    """
    Go back to the booking page
    """
    def back(self):
        # Create bokoing object
        booking = Booking(self.data)
        # This is to keep all the old data they inputted
        booking.time.setText(self.parent_data[1])
        booking.date.setText(self.parent_data[0])
        booking.symptoms_selected = self.getChecked()
        # Cleanup and change main frame
        self.destroy(destroySubWindows=True)
        self.parent().setCentralWidget(booking)
        self.deleteLater()

    """
    Get every selected checkbox
    """
    def getChecked(self):
        checked = []
        for i in self.checkbox_list:
            for j in i[list(i.keys())[0]]:
                if j.isChecked():
                    checked.append(j.text().lower())
        return checked
        
"""
Displays all the user's appointments
"""
class ViewAppointments(QtWidgets.QFrame):
    def __init__(self, data: dict):
        super().__init__()

        # Variables and elements
        self.data = data

        # Set the layout of the frame
        self.layout = QtWidgets.QVBoxLayout(self)

        self.header = QtWidgets.QLabel("Your Appointments", alignment=QtCore.Qt.AlignCenter)
        self.back = QtWidgets.QPushButton("Back")
        self.appointments = QtWidgets.QListWidget()
        self.delete_appointment = QtWidgets.QPushButton("Delete Appointment")
        self.user_calendar = QtWidgets.QPushButton("Calendar")
        self.edit_appointment = QtWidgets.QPushButton("Edit")
        self.error_label = QtWidgets.QLabel("No appointment selected")

        # Add elements to the frame
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.appointments)
        self.layout.addWidget(self.delete_appointment)
        self.layout.addWidget(self.user_calendar)
        self.layout.addWidget(self.edit_appointment)
        self.layout.addWidget(self.back)

        # Load in all the appointments
        self.loadAppointments()

        # Make the buttons do things
        self.back.clicked.connect(self.goBack)
        self.delete_appointment.clicked.connect(self.deleteAppointment)
        self.user_calendar.clicked.connect(self.calendar)
        self.edit_appointment.clicked.connect(self.edit)

    """
    Opens the edit page
    """
    def edit(self):
        self.error_label.setParent(None)
        try:
            temp_str = self.appointments.currentItem().text()
            temp_str = temp_str.strip().split(",")

            edit_page = Edit(self.data, temp_str[0].split(":")[1], [], [])
            self.destroy(destroySubWindows=True)
            self.parent().setCentralWidget(edit_page)
            self.deleteLater()
        except:
            self.layout.addWidget(self.error_label)

    """
    Goess back to the user's dashboard
    """
    def goBack(self):
        dashboard = DashBoard(self.data)
        self.destroy(destroySubWindows=True)
        self.parent().setCentralWidget(dashboard)
        self.deleteLater()

    """
    Loads all of the user's appointments
    """
    def loadAppointments(self):
        appointments = readFileJSON_Appointment(self.data["Username"])
        if appointments:
            for appointment in appointments:
                item = QtWidgets.QListWidgetItem(f"Date: {appointment['Date']}, Time: {appointment['Time']}, Reasons: {appointment['Reasons']}")
                self.appointments.addItem(item)
        else:
            self.appointments = []

    """
    Shows the user's appointments in the form of a calendar
    """
    def calendar(self):
        month = Month(datetime.today().strftime("%Y-%m-%d"), self.data)
        self.destroy(destroySubWindows=True)
        self.parent().setCentralWidget(month)
        self.deleteLater()

    """
    Deletes a selected appointment
    """
    def deleteAppointment(self):
        selected_item = self.appointments.currentItem()
        if selected_item:
            self.appointments.takeItem(self.appointments.row(selected_item))
            appointments = readFileJSON_Appointment(self.data["Username"])
            for appointment in appointments:
                # Check if the requested appointment is the same as the current appointment
                if f"Date: {appointment['Date']}, Time: {appointment['Time']}, Reasons: {appointment['Reasons']}" == selected_item.text():
                    # Delete
                    deleteApointmentJSON(appointment, self.data["Username"])
                    appointments.remove(appointment)
                    break

"""
The symptom select page when the user wants to edit an appointment
"""
class Symptoms1(Symptoms):
    def __init__(self, data: dict, parent_data: list, symptoms_selected: list, appointment_date: str):
        super().__init__(data, parent_data, symptoms_selected)
        
        # All elements and variabl
        self.appointment_date = appointment_date

        # Make the button do stuff
        self.back_btn.clicked.connect(self.back)

    """
    Go back to the previous page
    """
    def back(self):
        self.symptom_list = self.getChecked()
        edit = Edit(self.data, self.appointment_date, self.symptom_list, self.parent_data)
        self.parent().setCentralWidget(edit)
        self.destroy(destroySubWindows=True)
        self.deleteLater()

"""
Edit page for an appointment
"""
class Edit(QtWidgets.QFrame):
    def __init__(self, data: dict, appointment_date: str, symptoms: list, parent_data: list):
        super().__init__()

        # Set the layout of the frame
        self.layout = QtWidgets.QVBoxLayout(self)

        # All elements and variables
        self.data = data
        self.appointments = readFileJSON_Appointment(self.data["Username"])
        self.appointment = {}
        self.error_label = QtWidgets.QLabel("1 or more fields empty")

        # Get the appointment details
        for i in self.appointments:
            if appointment_date.strip()==i["Date"]:
                self.appointment = i
                break
        
        # Fill the text edits with the appointment details
        if parent_data:
            self.date = QtWidgets.QLineEdit(parent_data[0])
            self.time = QtWidgets.QLineEdit(parent_data[1])
            self.symptoms_selected = symptoms
        else:
            self.date = QtWidgets.QLineEdit(self.appointment["Date"])
            self.time = QtWidgets.QLineEdit(self.appointment["Time"])

        if symptoms:
            self.symptoms_selected = symptoms
        else:
            self.symptoms_selected = []
            for i in self.appointment["Reasons"]:
                self.symptoms_selected.append(i)
            
        self.symptoms_btn = QtWidgets.QPushButton("Reasons")
        self.back_btn = QtWidgets.QPushButton("Save and Back")

        # Add elements to the fram
        self.layout.addWidget(self.date)
        self.layout.addWidget(self.time)
        self.layout.addWidget(self.symptoms_btn)
        self.layout.addWidget(self.back_btn)

        # Make button do stuff
        self.back_btn.clicked.connect(self.back) 
        self.symptoms_btn.clicked.connect(self.viewSymptoms)

    """
    Let the user select symptoms
    """
    def viewSymptoms(self):
        symptoms = Symptoms1(self.data, [self.date.text(), self.time.text()], self.symptoms_selected, self.date.text())
        self.destroy(destroySubWindows=True)
        self.parent().setCentralWidget(symptoms)
        self.deleteLater()

    """
    Go back to the users appointment dashboard
    """
    def back(self):
        # Reset error label
        self.error_label.setParent(None)

        if self.verifyFields():
            # Get the data from the text fields
            appointment_date = self.date.text().split("-")
            appointment_date = datetime(int(appointment_date[0]), int(appointment_date[1]), int(appointment_date[2])).strftime("%Y-%m-%d")
            appointment_time = self.time.text()

            # Format all data
            new_appointment = {
                "Date": appointment_date,
                "Time": appointment_time,
                "Reasons": self.symptoms_selected
            }

            # Delete the old appointment and replace with the new appointment
            deleteApointmentJSON(self.appointment, self.data["Username"])
            temp = readFileJSON_Appointment(self.data["Username"])
            temp.append(new_appointment)
            writeFileJSON_Appointment(temp, self.data["Username"])

            # Change the main frame
            appointment_view = ViewAppointments(self.data)
            self.destroy(destroySubWindows=True)
            self.parent().setCentralWidget(appointment_view)
            self.deleteLater()
        else:
            # Error message
            self.layout.addWidget(self.error_label)

    """
    Check if the fields are completed
    """
    def verifyFields(self):
        if any(not field.text() for field in [self.date, self.time]):
            return False
        if not self.symptoms_selected:
            return False
        if not self.verifyDate(self.date.text()):
            return False
        if not self.verifyTime(self.time.text()):
            return False
        # They are all completed
        return True

    """
    Check and see if a given date is in the valid formt and if the day is in the past
    """
    def verifyDate(self, date: str):
        # Check if date is in the past
        date = date.strip()
        year, month, day = int(date.split("-")[0]), int(date.split("-")[1]), int(date.split("-")[2])
        if year <= datetime.today().year:
            if month <= datetime.today().month:
                if day < datetime.today().day: 
                    return False
                
        # Check if the numbers are valid
        try:
            t = datetime(year, month, day)
        except:
            return False
        
        # Check if formatted correctly
        pattern = r'^\d{4}-\d{1,2}-\d{1,2}$'
        return bool(re.match(pattern, date))

    """
    Check if the time is in the correct format
    """
    def verifyTime(self, time: str):
        pattern = r'^[012]*\d{1}:\d{2}$'
        return bool(re.match(pattern, time))

"""
The user's setting page
"""
class Settings(QtWidgets.QFrame):
    def __init__(self, data: dict):
        super().__init__()

        # All elements and variables
        self.data = data
        self.header = QtWidgets.QLabel("Settings", alignment=QtCore.Qt.AlignCenter)
        self.change_credentials = QtWidgets.QPushButton("Change Username/Password")
        self.back_btn = QtWidgets.QPushButton("Save and Back")

        # Set the layout of the frame
        self.layout = QtWidgets.QVBoxLayout(self)

        # Add all elements to the frame
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.change_credentials)
        self.layout.addWidget(self.back_btn)

        # Make buttons do stuff
        self.change_credentials.clicked.connect(self.changeCredentials)
        self.back_btn.clicked.connect(self.back)
    
    """
    Change the page to the username and password page
    """
    def changeCredentials(self):
        page = SignUp1(self.data)
        self.destroy(destroySubWindows=True)
        self.parent().setCentralWidget(page)
        self.deleteLater()

    """
    Go back to the user's dashboard
    """
    def back(self):
        dashboard = DashBoard(self.data)
        self.destroy(destroySubWindows=True)
        self.parent().setCentralWidget(dashboard)
        self.deleteLater()

"""
Main function of the program
"""
if __name__ == "__main__":
    # Create the app
    app = QtWidgets.QApplication([])
    
    # Create the main frame
    main = Window()
    # Show the window
    main.show()

    # End program when user closes window
    sys.exit(app.exec())