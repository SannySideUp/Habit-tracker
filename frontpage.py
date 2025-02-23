from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
import os
import sys
import pyrebase

# Firebase configuration settings
firebaseConfig = {
    "apiKey": "AIzaSyCx6-n1Zo-VXBPx8mPcXsDsSqt6sUFqTFI",
    "authDomain": "habit-9fe64.firebaseapp.com",
    "databaseURL": "https://habit-9fe64-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "habit-9fe64",
    "storageBucket": "habit-9fe64.firebasestorage.app",
    "messagingSenderId": "260772887006",
    "appId": "1:260772887006:web:8979f4f4320240e75a054f",
    "measurementId": "G-P2FHLC3000"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
databases = firebase.database()  # Reference to Firebase Realtime Database
authfire = firebase.auth()  # Firebase authentication reference

class Login(QMainWindow):
    """Login window where users enter their email and password to log in."""

    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "login.ui"), self)  # Load the UI file
        self.show()

        # Connect buttons to their functions
        self.pushButton.clicked.connect(self.login)  # Login button
        self.signupbutton.clicked.connect(self.goCreateAccount)  # Signup button

    def login(self):
        """Handles user login authentication using Firebase."""
        email = self.email.text()
        password = self.password.text()
        
        try:
            authfire.sign_in_with_email_and_password(email, password)  # Authenticate user
            login_successful = True  # If authentication succeeds, set login to True
        except:
            login_successful = False  # If authentication fails, set login to False

        print(login_successful)  # Debugging print statement

        if login_successful:
            widget.setCurrentIndex(2)  # Switch to the Habit Tracker page
        else:
            # Show error message for invalid login credentials
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText("Invalid ID")
            error.setWindowTitle("Login Error")
            error.exec_()
    
    def goCreateAccount(self):
        """Switch to the Signup window."""
        widget.setCurrentIndex(1)

class CreateAcc(QMainWindow):
    """Signup window where users create an account."""

    def __init__(self):
        super(CreateAcc, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "SignUp.ui"), self)  # Load UI file
        
        # Ensure these input fields exist in SignUp.ui
        self.password.setEchoMode(QLineEdit.Password)  # Hide password input
        self.confirmPassword.setEchoMode(QLineEdit.Password)  # Hide confirm password input

        # Connect signup button to create account function
        self.signupbutton.clicked.connect(self.createAccountFunction)
    
    def createAccountFunction(self):
        """Handles new user account creation with Firebase."""
        email = self.email.text()  # Get email input
        password = self.password.text()
        confirm_password = self.confirmPassword.text()

        if password == confirm_password and len(password) > 4:
            # Passwords match and meet the length requirement
            print(f"Successfully created account with email: {email}")
            authfire.create_user_with_email_and_password(email, password)  # Create user in Firebase
            
            widget.setCurrentIndex(0)  # Switch back to login screen
        else:
            # Show error message for mismatched or short passwords
            error = QMessageBox()
            error.setIcon(QMessageBox.Warning)
            error.setText("Passwords do not match or Password is too short!")
            error.setWindowTitle("Signup Error")
            error.exec_()

class HabitTracker(QMainWindow):
    """Habit Tracker application window."""

    def __init__(self):
        super(HabitTracker, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "HabitTracker.ui"), self)  # Load UI file
        self.show()

        # Connect button to function
        self.pushButton_2.clicked.connect(lambda: self.sayit(self.textEdit.toPlainText()))
    
    def sayit(self, msg):
        """Displays a message in a pop-up window."""
        message = QMessageBox()
        message.setText(msg)
        message.exec_()

# Initialize the QApplication and QStackedWidget for navigation between pages
app = QApplication(sys.argv)
widget = QStackedWidget()

# Create instances of the pages
mainWindow = Login()  # Login page
createAccountWindow = CreateAcc()  # Signup page
habitTrackerWindow = HabitTracker()  # Habit Tracker page

# Add pages to the stacked widget
widget.addWidget(mainWindow)  # Index 0: Login page
widget.addWidget(createAccountWindow)  # Index 1: Signup page
widget.addWidget(habitTrackerWindow)  # Index 2: Habit Tracker page

# Set up and display the main application window
widget.setFixedHeight(400)
widget.setFixedWidth(600)
widget.show()

# Start the application event loop
sys.exit(app.exec_())
