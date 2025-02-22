from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
import os
import sys
import pyrebase

# Firebase Configuration
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

firebase = pyrebase.initialize_app(firebaseConfig)
databases = firebase.database()
authfire = firebase.auth()

# --------------------- Twitter-Style UI ---------------------
TWITTER_BLUE = "#1DA1F2"
DARK_MODE = "#15202B"
LIGHT_MODE = "#FFFFFF"
TEXT_COLOR_LIGHT = "#000000"
TEXT_COLOR_DARK = "#FFFFFF"
# --------------------- Frontpage Window ---------------------

class frontpage(QMainWindow):
    def __init__(self):
        super(frontpage, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "welcome page.ui"), self)

        self.setStyleSheet(f"""
            background-color: {DARK_MODE};
            color: {TEXT_COLOR_DARK};
            font-family: 'Segoe UI', Arial, sans-serif;
        """)

        self.login.setStyleSheet(f"""
            QPushButton {{
                background-color: {TWITTER_BLUE};
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 25px;
                padding: 10px;
                width: 250px;
            }}
            QPushButton:hover {{
                background-color: #0D8AEF;
            }}
        """)

        self.signUp.setStyleSheet(f"""
            QPushButton {{
                background-color: {TWITTER_BLUE};
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 25px;
                padding: 10px;
                width: 250px;
            }}
            QPushButton:hover {{
                background-color: #0D8AEF;
            }}
        """)

        self.login.clicked.connect(self.loginButton)
        self.signUp.clicked.connect(self.signUpButton)

    def loginButton(self):
            widget.setCurrentIndex(1)

    def signUpButton(self):
            widget.setCurrentIndex(2)

# --------------------- Login Window ---------------------
class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "login.ui"), self)

        self.setStyleSheet(f"""
            background-color: {DARK_MODE};
            color: {TEXT_COLOR_DARK};
            font-family: 'Segoe UI', Arial, sans-serif;
        """)

        self.pushButton.setStyleSheet(f"""
            QPushButton {{
                background-color: {TWITTER_BLUE};
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 25px;
                padding: 10px;
                width: 250px;
            }}
            QPushButton:hover {{
                background-color: #0D8AEF;
            }}
        """)

        self.signupbutton.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {TWITTER_BLUE};
                font-size: 14px;
                border: none;
            }}
            QPushButton:hover {{
                text-decoration: underline;
            }}
        """)

        # Placeholder Text
        self.email.setPlaceholderText("Email or Username")
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.pushButton.clicked.connect(self.login)
        self.signupbutton.clicked.connect(self.goCreateAccount)
        self.checkBox.clicked.connect(self.showPassword)

    def login(self):
        email = self.email.text()
        password = self.password.text()
        if not email or not password:
            self.showError("Both fields are required!")
            return

        try:
            authfire.sign_in_with_email_and_password(email, password)
            widget.setCurrentIndex(3)
        except:
            self.showError("Invalid Email or Password!")

    def goCreateAccount(self):
        widget.setCurrentIndex(2)

    def showError(self, message):
        error = QMessageBox()
        error.setIcon(QMessageBox.Critical)
        error.setText(message)
        error.setWindowTitle("Error")
        error.exec_()
    
    def showPassword(self):
        if self.checkBox.isChecked():
            self.password.setEchoMode(QLineEdit.Normal)
        else:
            self.password.setEchoMode(QLineEdit.Password)


# --------------------- Sign Up Window ---------------------
class CreateAcc(QMainWindow):
    def __init__(self):
        super(CreateAcc, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "SignUp.ui"), self)

        self.setStyleSheet(f"""
            background-color: {DARK_MODE};
            color: {TEXT_COLOR_DARK};
            font-family: 'Segoe UI', Arial, sans-serif;
        """)

        self.signupbutton.setStyleSheet(f"""
            QPushButton {{
                background-color: {TWITTER_BLUE};
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 25px;
                padding: 10px;
                width: 250px;
            }}
            QPushButton:hover {{
                background-color: #0D8AEF;
            }}
        """)

        # Placeholder text
        self.name.setPlaceholderText("Your Name")
        self.email.setPlaceholderText("Your Email")
        self.password.setPlaceholderText("Create a Password")
        self.confirmPassword.setPlaceholderText("Confirm Password")

        self.password.setEchoMode(QLineEdit.Password)
        self.confirmPassword.setEchoMode(QLineEdit.Password)

        self.signupbutton.clicked.connect(self.createAccountFunction)

    def createAccountFunction(self):
        email = self.email.text()
        password = self.password.text()
        confirm_password = self.confirmPassword.text()

        if not email or not password or not confirm_password:
            self.showError("All fields are required!")
            return

        if password != confirm_password:
            self.showError("Passwords do not match!")
            return

        if len(password) < 6:
            self.showError("Password must be at least 6 characters!")
            return

        try:
            authfire.create_user_with_email_and_password(email, password)
            widget.setCurrentIndex(1)
        except:
            self.showError("Account creation failed. Try again.")

    def showError(self, message):
        error = QMessageBox()
        error.setIcon(QMessageBox.Warning)
        error.setText(message)
        error.setWindowTitle("Signup Error")
        error.exec_()


# --------------------- Habit Tracker Window ---------------------
class HabitTracker(QMainWindow):
    def __init__(self):
        super(HabitTracker, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "HabitTracker.ui"), self)

        self.setStyleSheet(f"""
            background-color: {DARK_MODE};
            color: {TEXT_COLOR_DARK};
            font-family: 'Segoe UI', Arial, sans-serif;
        """)

        self.pushButton_2.setStyleSheet(f"""
            QPushButton {{
                background-color: {TWITTER_BLUE};
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 25px;
                padding: 10px;
                width: 250px;
            }}
            QPushButton:hover {{
                background-color: #0D8AEF;
            }}
        """)

        self.show()
        self.pushButton_2.clicked.connect(lambda: self.sayit(self.textEdit.toPlainText()))

    def sayit(self, msg):
        if msg.strip():
            message = QMessageBox()
            message.setText(msg)
            message.exec_()
            databases.child("database").child("Users").update("habits",msg)
        else:
            self.showError("Please enter a message!")

    def showError(self, message):
        error = QMessageBox()
        error.setIcon(QMessageBox.Warning)
        error.setText(message)
        error.setWindowTitle("Error")
        error.exec_()


# --------------------- App Initialization ---------------------
app = QApplication(sys.argv)
widget = QStackedWidget()

welcome = frontpage()
mainWindow = Login()
createAccountWindow = CreateAcc()
App = HabitTracker()

widget.addWidget(welcome)
widget.addWidget(mainWindow)
widget.addWidget(createAccountWindow)
widget.addWidget(App)

widget.setFixedHeight(300)
widget.setFixedWidth(500)
widget.show()

sys.exit(app.exec_())
