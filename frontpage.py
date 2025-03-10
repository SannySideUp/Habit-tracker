from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic, QtGui
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor, QPalette
import os
import sys
import pyrebase
from PyQt5.QtWidgets import QDialog, QPushButton, QListWidget, QListWidgetItem, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
import os
import datetime
from collections import Counter as counter

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

HONEYCOMB_STYLESHEET = """
    QDialog {
        background-color: #F4D03F;  /* Yellow background */
    }

    QLabel {
        color: #654321;  /* Brown text */
        font-family: 'Comic Sans MS';
        font-size: 24px;
    }

    QPushButton {
        background-color: #D4AC0D;  /* Dark yellow */
        color: #654321;  /* Brown text */
        border: 2px solid #654321;
        border-radius: 15px;
        padding: 10px;
        font-family: 'Comic Sans MS';
        font-size: 18px;
    }

    QPushButton:hover {
        background-color: #F1C40F;  /* Lighter yellow on hover */
    }

    QListWidget {
        background-color: #F9E79F;  /* Light yellow */
        color: #654321;  /* Brown text */
        border: 2px solid #654321;
        border-radius: 10px;
        font-family: 'Comic Sans MS';
        font-size: 16px;
    }

    QListWidget::item {
        padding: 10px;
        border-bottom: 1px solid #654321;  /* Brown separator */
    }

    QListWidget::item:selected {
        background-color: #D4AC0D;  /* Dark yellow for selected items */
        color: #654321;  /* Brown text */
    }
"""

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
DARK_MODE_BG = "#15202B"
LIGHT_MODE_BG = "#FFFFFF"
TEXT_COLOR_LIGHT = "#000000"
TEXT_COLOR_DARK = "#FFFFFF"

# --------------------- Login Window ---------------------
class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "login.ui"), self)
        #added userID field
        self.userID  = ""
        self.setStyleSheet(f"""
            background-color: {DARK_MODE_BG};
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
        global email
        email = self.email.text()
        password = self.password.text()
        if not email or not password:
            self.showError("Both fields are required!")
            return

        try:
            authfire.sign_in_with_email_and_password(email, password)
            #get userID
            user = authfire.current_user
            self.userID = user['localId']
            #pass userID to welcome screen
            welcome_screen = WelcomeScreen(self.userID)
            widget.addWidget(welcome_screen)
            widget.setCurrentWidget(welcome_screen)
        except:
            self.showError("Invalid Email or Password!")
            
    def goCreateAccount(self):
        widget.setCurrentIndex(1)
   
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
            background-color: {DARK_MODE_BG};
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

        self.backToLogin.setStyleSheet(f"""
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

        # Placeholder text
        self.name.setPlaceholderText("Your Name")
        self.email.setPlaceholderText("Your Email")
        self.password.setPlaceholderText("Create a Password")
        self.confirmPassword.setPlaceholderText("Confirm Password")

        self.password.setEchoMode(QLineEdit.Password)
        self.confirmPassword.setEchoMode(QLineEdit.Password)
        self.signupbutton.clicked.connect(self.createAccountFunction)
        self.backToLogin.clicked.connect(self.go_back_to_login)

    def createAccountFunction(self):
        email = self.email.text()
        password = self.password.text()
        confirm_password = self.confirmPassword.text()
        name = self.name.text() ###get user's name
        
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
            user = authfire.create_user_with_email_and_password(email, password)
            userID = user['localId']
            self.add_username(databases,userID,name)
            widget.setCurrentIndex(0)
        except:
            self.showError("Account creation failed. Try again.")

    def showError(self, message):
        error = QMessageBox()
        error.setIcon(QMessageBox.Warning)
        error.setText(message)
        error.setWindowTitle("Signup Error")
        error.exec_()

    def add_username(self, db, UUID, name): #add user name to display on welcome screen
        db.child(UUID).child("name").push(name)

    def go_back_to_login(self):
        widget.setCurrentIndex(0)  # Switch back to the login screen



# --------------------- WelcomeScreen Window ---------------------
class WelcomeScreen(QMainWindow):
    def __init__(self,userID):
        super(WelcomeScreen, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "WelcomeScreen.ui"), self)
        self.userID = userID #add userID

        # Apply the background and text styles for the entire window
        self.setStyleSheet(f"""
            background-color: {DARK_MODE_BG};
            color: {TEXT_COLOR_DARK};
            font-family: 'Segoe UI', Arial, sans-serif;
        """)

        # Apply the button styles
        self.AddHabit.setStyleSheet(f"""
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
        
        self.DeleteHabit.setStyleSheet(f"""
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

        self.ViewHabit.setStyleSheet(f"""
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

        self.LogOut.setStyleSheet(f"""
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

        self.Calendar.setStyleSheet(f"""
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
            QCalendarWidget {{
                background-color: {TWITTER_BLUE};
            }}
        """)
        
        self.Streaks.setStyleSheet(f"""
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

        # Connections
        self.AddHabit.clicked.connect(self.on_add_habit)
        self.DeleteHabit.clicked.connect(self.on_delete_habit)
        self.LogOut.clicked.connect(self.BackToLogin)
        self.ViewHabit.clicked.connect(self.view_habits) 
        self.Calendar.clicked.connect(self.show_calendar)
        self.Streaks.clicked.connect(self.show_streaks)
        


    def on_add_habit(self):
        self.add_habit = AddHabit(self.userID)#pass userID to addHabit
        self.add_habit.show()
    
    def show_calendar(self):
        calendar_dialog = CalendarDialog()  # Create the calendar dialog
        calendar_dialog.exec_()

    def view_habits(self):
        self.view_habits_window = ViewHabitScreen(self.userID)
        self.view_habits_window.exec_()
        

    def on_delete_habit(self):
        self.delete_habit = DeleteHabit(self.userID)#pass userID to deleteHabit
        self.delete_habit.exec_()  # Show the DeleteHabit dialog

    def BackToLogin(self):
        widget.setCurrentIndex(0)

    def show_streaks(self):
        """Create and show the Streak dialog."""
        self.streak_dialog = Streak(self.userID, self)  # Pass self as the welcome_screen argument
        self.hide()  # Hide the WelcomeScreen
        self.streak_dialog.exec_()  # Show the Streak dialog as a modal window
        self.show()

    
        

# --------------------- ViewHabit Screen -------------------- 
class ViewHabitScreen(QDialog):
    def __init__(self, userID):
        super(ViewHabitScreen, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "ViewHabit.ui"), self)
        self.userID = userID  # Store userID

        # Set up UI elements
        self.setStyleSheet("background-color: #15202B; color: white;")
        self.habit_list = self.findChild(QListWidget, "habit_list") 
        self.close_button = self.findChild(QPushButton, "closebutton")  

        # Connect buttons
        if self.close_button:
            self.close_button.clicked.connect(self.close)

        # Load habits initially
        self.load_habits()

    def load_habits(self):
        self.habit_list.clear()  # Clear existing habits
        try:
            habits = databases.child(self.userID).child("habits").get()
            if habits.each():
                for habit in habits.each():
                    habit_data = habit.val()
                    habit_text = f"{habit_data['title']} - {habit_data['start_date']} ({habit_data['difficulty']})"
                    self.habit_list.addItem(habit_text)  # Add habit to the list
            else:
                self.habit_list.addItem("No habits found.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load habits: {str(e)}")

#========================================================================================================




class Streak(QDialog):
    def __init__(self, userID, welcome_screen):
        super(Streak, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "Streaks.ui"), self)
        self.userID = userID
        self.welcome_screen = welcome_screen  # Store the WelcomeScreen instance
        self.setStyleSheet(HONEYCOMB_STYLESHEET)

        # Find the streakCounter label
        self.streakCounter = self.findChild(QLabel, "streakCounter")
        if not self.streakCounter:
            print("Error: streakCounter label not found")

        # Find the "back" button in the UI
        self.back = self.findChild(QPushButton, "back")  # Use the correct objectName
        if self.back:
            self.back.clicked.connect(self.go_back_to_welcome_screen)
        else:
            print("Error: 'back' button not found in the UI file.")

        # Find the "update" button in the UI
        self.updateButton = self.findChild(QPushButton, "updateStreak")  # Replace with your button's objectName
        if self.updateButton:
            self.updateButton.clicked.connect(self.open_update_streaks)
        else:
            print("Error: 'updateButton' not found in the UI file.")

        # Load the current streak counter
        self.load_streak_counter()

    def go_back_to_welcome_screen(self):
        """Close the Streak dialog and show the WelcomeScreen."""
        self.close()  # Close the Streak dialog
        self.welcome_screen.show()  # Show the WelcomeScreen

    def open_update_streaks(self):
        """Open the UpdateStreaks dialog."""
        self.update_streaks_dialog = UpdateStreaks(self.userID, self)  # Pass self (Streak dialog) to UpdateStreaks
        self.update_streaks_dialog.exec_()  # Show the UpdateStreaks dialog as a modal window

    def load_streak_counter(self):
        """Load the current streak counter from the database and update the label."""
        try:
            streak_data = databases.child(self.userID).child("streakCounter").get()
            if streak_data.val() is not None:
                self.streakCounter.setText(str(streak_data.val()))
            else:
                self.streakCounter.setText("0")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load streak counter: {str(e)}")









class UpdateStreaks(QDialog):
    def __init__(self, userID, streak_dialog):
        super(UpdateStreaks, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "updateStreaks.ui"), self)
        self.userID = userID
        self.streak_dialog = streak_dialog  # Store the Streak dialog reference
        self.setStyleSheet(HONEYCOMB_STYLESHEET)


        # Debug: Print all child widgets to verify the buttons exist
        print("Child widgets:", self.findChildren(QPushButton))

        # Find the addStreak button
        self.addStreak = self.findChild(QPushButton, "addStreak")
        if self.addStreak:
            print("addStreak button found")
            self.addStreak.clicked.connect(self.on_add_streak)
            self.addStreak.setEnabled(False)  # Disable the button initially
        else:
            print("Error: addStreak button not found")

        # Find the BACK button
        self.backToStreaks = self.findChild(QPushButton, "backToStreaks")
        if self.backToStreaks:
            print("BACK button found")
            self.backToStreaks.clicked.connect(self.close)
        else:
            print("Error: BACK button not found")

        # Load habits into the habit_list widget
        self.load_habits()

        # Connect the itemChanged signal to check if all checkboxes are checked
        self.habit_list.itemChanged.connect(self.check_all_checked)

        # Check if the user can check the boxes (24-hour rule)
        self.check_24_hour_rule()

    def load_habits(self):
        """Load habits from the database and display them in the habit_list widget with checkboxes."""
        self.habit_list.clear()  # Clear existing habits
        try:
            habits = databases.child(self.userID).child("habits").get()
            if habits.each():
                for habit in habits.each():
                    habit_data = habit.val()
                    habit_text = f"{habit_data['title']} - {habit_data['start_date']} ({habit_data['difficulty']})"
                    item = QListWidgetItem(habit_text)
                    item.setCheckState(Qt.Unchecked)  # Add a checkbox
                    self.habit_list.addItem(item)  # Add habit to the list
            else:
                self.habit_list.addItem("No habits found.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load habits: {str(e)}")

    def check_all_checked(self):
        """Check if all checkboxes are checked and enable/disable the addStreak button."""
        all_checked = True
        for index in range(self.habit_list.count()):
            item = self.habit_list.item(index)
            if item.checkState() != Qt.Checked:
                all_checked = False
                break
        self.addStreak.setEnabled(all_checked)  # Enable the button only if all checkboxes are checked

    def check_24_hour_rule(self):
        """Check if the user can check the boxes (24-hour rule)."""
        try:
            last_checked_time = databases.child(self.userID).child("lastCheckedTime").get()
            if last_checked_time.val():
                last_checked = datetime.datetime.fromisoformat(last_checked_time.val())
                current_time = datetime.datetime.now()
                time_diff = (current_time - last_checked).total_seconds()

                if time_diff < 86400:  # 24 hours in seconds
                    # Disable checkboxes if less than 24 hours have passed
                    for index in range(self.habit_list.count()):
                        item = self.habit_list.item(index)
                        item.setFlags(item.flags() & ~Qt.ItemIsEnabled)  # Disable the checkbox
                    self.addStreak.setEnabled(False)
                    QMessageBox.information(self, "Info", "You can only check the boxes once every 24 hours.")
                else:
                    # Reset the streak counter if more than 24 hours have passed
                    databases.child(self.userID).child("streakCounter").set(0)
                    self.streak_dialog.streakCounter.setText("0")
                    QMessageBox.information(self, "Info", "Streak reset to 0 because you missed the 24-hour window.")
            else:
                # No last checked time, allow the user to check the boxes
                pass
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to check 24-hour rule: {str(e)}")

    def on_add_streak(self):
        """Handle the ADD STREAK button click."""
        try:
            # Increment the streakCounter in the database
            streak_data = databases.child(self.userID).child("streakCounter").get()
            if streak_data.val() is None:
                streak_counter = 1
            else:
                streak_counter = streak_data.val() + 1
            databases.child(self.userID).child("streakCounter").set(streak_counter)

            # Update the streakCounter label in the Streak dialog
            self.streak_dialog.streakCounter.setText(str(streak_counter))

            # Update the last checked time
            current_time = datetime.datetime.now().isoformat()
            databases.child(self.userID).child("lastCheckedTime").set(current_time)

            # Disable checkboxes for 24 hours
            for index in range(self.habit_list.count()):
                item = self.habit_list.item(index)
                item.setFlags(item.flags() & ~Qt.ItemIsEnabled)  # Disable the checkbox
            self.addStreak.setEnabled(False)

            # Show a success message
            QMessageBox.information(self, "Success", f"Streak incremented to {streak_counter}!")

            # Schedule a timer to re-enable checkboxes after 24 hours
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.reset_checkboxes)
            self.timer.start(86400000)  # 24 hours in milliseconds
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update streak: {str(e)}")

    def reset_checkboxes(self):
        """Re-enable checkboxes after 24 hours."""
        for index in range(self.habit_list.count()):
            item = self.habit_list.item(index)
            item.setFlags(item.flags() | Qt.ItemIsEnabled)  # Re-enable the checkbox
        self.timer.stop()  # Stop the timer


    

    




       


# --------------------- Calendar button  -------------------- 
class CalendarDialog(QDialog):
    def __init__(self):
        super(CalendarDialog, self).__init__()

        # Set window title and size
        self.setWindowTitle("Calendar")
        self.setFixedSize(600, 600)
        
        # Create the calendar widget
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        
        # Create the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.calendar)

        # Add a close button
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)
        
        self.setLayout(layout)

# --------------------- AddHabit Dialogue --------------------

class AddHabit(QDialog):
    # Signal to close the dialog
    close_dialog_signal = pyqtSignal()

    def __init__(self,userID):
        super(AddHabit, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "AddHabit.ui"), self)
        self.userID = userID # add userID

        # Connect the signal to the accept() method
        self.close_dialog_signal.connect(self.accept)

        # Set background color and text color
        self.setStyleSheet(f"""
            background-color: {DARK_MODE_BG};
            color: {TEXT_COLOR_DARK};
            font-family: 'Segoe UI', Arial, sans-serif;
        """)

        # Set the style for the TitleInput (QLineEdit) with hover effect and dark blue input text
        self.TitleInput.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 5px;
                color: #1D3C6A;  
            }
            QLineEdit:hover {
                background-color: #D9F1FF;  
            }
        """)

        # Set the style for the DescriptionInput (QTextEdit) with hover effect and dark blue input text
        self.DescriptionInput.setStyleSheet("""
            QTextEdit {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 5px;
                color: #1D3C6A;  
            }
            QTextEdit:hover {
                background-color: #D9F1FF;  
            }
        """)

        # Set the style for the RepeatsBox (QComboBox) with hover effect and visible text
        self.RepeatsBox.setStyleSheet("""
            QComboBox {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 5px;
                color: #1D3C6A;  
            }
            QComboBox:hover {
                background-color: #D9F1FF;  
            }
            QComboBox:editable {
                color: #1D3C6A;  
            }
        """)

        # Set the style for the DifficultyBox (QComboBox) with hover effect and visible text
        self.DifficultyBox.setStyleSheet("""
            QComboBox {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 5px;
                color: #1D3C6A;  
            }
            QComboBox:hover {
                background-color: #D9F1FF;  
            }
            QComboBox:editable {
                color: #1D3C6A;  
            }
        """)

        # Set the style for the Save and Cancel buttons
        save_button = self.CancelSaveBox.button(QDialogButtonBox.Save)
        cancel_button = self.CancelSaveBox.button(QDialogButtonBox.Cancel)

        save_button.setStyleSheet("""
            QPushButton {
                background-color: #A1D6FF;  
                border: 1px solid #4A90E2;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #91C9FF;  
            }
        """)

        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #A1D6FF;  
                border: 1px solid #4A90E2;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #91C9FF;  
            }
        """)

        # Set labels (DescriptionLabel, DifficultyLabel, RepeatsLabel, StartDateLabel, TitleLabel)
        self.DescriptionLabel.setStyleSheet("""
            QLabel {
                font-weight: bold;
            }
        """)
        
        self.DifficultyLabel.setStyleSheet("""
            QLabel {
                font-weight: bold;
            }
        """)

        self.RepeatsLabel.setStyleSheet("""
            QLabel {
                font-weight: bold;
            }
        """)

        self.StartDateLabel.setStyleSheet("""
            QLabel {
                font-weight: bold;
            }
        """)

        self.TitleLabel.setStyleSheet("""
            QLabel {
                font-weight: bold;
            }
        """)

        # Connect buttons
        save_button.clicked.connect(self.saveHabit)
        cancel_button.clicked.connect(self.reject)

    def saveHabit(self):
        save_button = self.CancelSaveBox.button(QDialogButtonBox.Save)
        save_button.setEnabled(False)

        # Retrieve the input values
        title = self.TitleInput.text()
        description = self.DescriptionInput.toPlainText()
        start_date = self.CalenderWidget.selectedDate().toString("yyyy-MM-dd")
        repeat = self.RepeatsBox.currentText()
        difficulty = self.DifficultyBox.currentText()

        if not title or not description:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields")
            save_button.setEnabled(True)
            return
        
        # Save to Firebase
        habit_data = {
            "title": title,
            "description": description,
            "start_date": start_date,
            "repeat": repeat,
            "difficulty": difficulty
        }

        # Firebase save operation
        try:
            databases.child(self.userID).child("habits").push(habit_data)#change node
            QMessageBox.information(self, "Success", "Habit added successfully!")
            self.close_dialog_signal.emit()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add habit: {str(e)}")
            save_button.setEnabled(True)

# --------------------- DeleteHabit Dialogue --------------------

class DeleteHabit(QDialog):
    def __init__(self,userID): #add user ID
        super(DeleteHabit, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "DeleteHabit.ui"), self)
        self.userID = userID #add user ID
        # Set styles
        self.setStyleSheet(f"""
            background-color: {DARK_MODE_BG};
            color: {TEXT_COLOR_DARK};
            font-family: 'Segoe UI', Arial, sans-serif;
        """)

        # Access the QListWidget and QPushButton
        self.habit_list = self.findChild(QListWidget, "habit_list")
        self.delete_button = self.findChild(QPushButton, "delete_button")

        # Connect the delete button to a function
        self.delete_button.clicked.connect(self.delete_selected_habit)

        # Load habits into the list
        self.fetch_habits()

    def fetch_habits(self):
        try:
            habits = databases.child(self.userID).child("habits").get() #get user's habits
            if habits.each() is not None:
                self.habit_list.clear()  # Clear the list before adding new items
                for habit in habits.each():
                    habit_data = habit.val()
                    habit_text = f"{habit_data['title']}"  # Display only the title
                    item = QListWidgetItem(habit_text)
                    item.setData(Qt.UserRole, habit.key())  # Store habit ID in the item
                    self.habit_list.addItem(item)  # Add habit to the list widget
            else:
                print("No habits found in the database.")
        except Exception as e:
            print("Failed to fetch habits:", str(e))

    def delete_selected_habit(self):
        selected_habit = self.habit_list.currentItem()
        if not selected_habit:
            QMessageBox.warning(self, "Error", "Please select a habit to delete.")
            return
        
        habit_id = selected_habit.data(Qt.UserRole)

        if habit_id is None:
            QMessageBox.critical(self, "Error", "Invalid habit selected.")
            return

        try:
            databases.child(self.userID).child("habits").child(habit_id).remove() #added userID
            QMessageBox.information(self, "Success", "Habit deleted successfully!")
            self.fetch_habits()  # Refresh the list after deletion
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete habit: {str(e)}")

# --------------------- App Initialization ---------------------
app = QApplication(sys.argv)
widget = QStackedWidget()
mainWindow = Login()
createAccountWindow = CreateAcc()

widget.addWidget(mainWindow)
widget.addWidget(createAccountWindow)

widget.setFixedHeight(500)
widget.setFixedWidth(650)
widget.show()

sys.exit(app.exec_())

# --------------------- App Initialization ---------------------
app = QApplication(sys.argv)
widget = QStackedWidget()

mainWindow = Login()
createAccountWindow = CreateAcc()
#welcome_screen = WelcomeScreen()


widget.addWidget(mainWindow)
widget.addWidget(createAccountWindow)
#widget.addWidget(welcome_screen)

widget.setFixedHeight(500)
widget.setFixedWidth(650)
widget.show()

sys.exit(app.exec_())


