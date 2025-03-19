from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic, QtGui
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor, QPalette
import ctypes
import os
import sys
import pyrebase
from PyQt5.QtWidgets import QDialog, QPushButton, QListWidget, QListWidgetItem, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
import datetime
from collections import Counter as counter
from google import genai
from google.genai import types
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

HONEYCOMB_STYLESHEET = """
    QMainWindow{
        background-color: #F9E79F;  /* Light yellow */
        color: #654321;  /* Brown text */
        border: 2px solid #654321;
        border-radius: 10px;
        font-family: 'Comic Sans MS';
        font-size: 16px;
    }
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
        border: 1px solid #654321;
        border-radius: 16px;
        padding: 12px;
        font-family: 'Comic Sans MS';
        font-size: 16px;
        min-width: 20px;
        min-height: 15px;
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

#client = genai.Client(api_key="AIzaSyAC1frMF9t4FO9jld2-EhLJezzRafVc7Eg")
#Response = client.models.generate_content(model="gemini-2.0-flash", contents=f"Give me the qoute of the day, also it should not be longer than 10 words also, IF AND ONLY IF it is not any of these quotes {all_quotes}")

# Google API
AI_quotes = []
User_quotes = []

try:
    quotes = databases.child("Quote").get()
    quotes_data = quotes.val()

    if quotes_data is not None:
        if isinstance(quotes_data, dict):
            for key in quotes_data:
                AI_quotes.append(quotes_data[key])
        else:
            print("No quotes found in the database.")
except Exception as e:
    print(e)
client = genai.Client(api_key="AIzaSyAC1frMF9t4FO9jld2-EhLJezzRafVc7Eg")
Response = client.models.generate_content(model="gemini-2.0-flash", contents=f"Give me the qoute of the day, also it should not be longer than 10 words also, IF AND ONLY IF it is not any of these quotes {AI_quotes}")
#if Response.text not in AI_quotes:
#    databases.child("Quote").push(Response.text)

UQuotes = databases.child("UserQuotes").get().val()

if UQuotes is not None:
    if isinstance(UQuotes,dict):
        for key in UQuotes:
            EachQuote = databases.child("UserQuotes").child(key).get().val()
            for User_ in EachQuote:
                names = databases.child("UserQuotes").child(key).child(User_).get().key()
                TheirQuotes = databases.child("UserQuotes").child(key).child(User_).get().val()
                User_quotes.append({names:TheirQuotes})

if AI_quotes and User_quotes:
    if random.choice([True, False]):  
        selected_quote = random.choice(AI_quotes)
        if Response.text not in AI_quotes:
            databases.child("Quote").push(Response.text)
    else:
        user_entry = random.choice(User_quotes)
        username, quote = next(iter(user_entry.items()))
        selected_quote = f'"{quote}" - By user: {username}'
elif AI_quotes:
    selected_quote = random.choice(AI_quotes)
    if Response.text not in AI_quotes:
        databases.child("Quote").push(Response.text)
else:
    user_entry = random.choice(User_quotes)
    username, quote = next(iter(user_entry.items()))
    selected_quote = f'"{quote}" - By user: {username}'

print(f"Today's Quote: {selected_quote}")

# --------------------- Login Window ---------------------
class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "login.ui"), self)
        self.setWindowTitle("Habit Tracker")
        self.userID = ""
        self.setStyleSheet(HONEYCOMB_STYLESHEET)

        self.email.setPlaceholderText("Email")
        self.password.setPlaceholderText("Password")

        self.password.setEchoMode(QLineEdit.Password)
        self.pushButton.clicked.connect(self.login)
        self.signupbutton.clicked.connect(self.goCreateAccount)
        self.checkBox.clicked.connect(self.showPassword)
        self.forgotPassword.clicked.connect(self.ForgetPassword)
        
        self.email.returnPressed.connect(self.focusPassword)
        self.password.returnPressed.connect(self.login)

    def login(self):
        email = self.email.text()
        password = self.password.text()
        if not email or not password:
            self.showError("Both fields are required!")
            return

        try:
            user = authfire.sign_in_with_email_and_password(email, password)
            user_info = authfire.get_account_info(user['idToken'])
            
            if not user_info['users'][0]['emailVerified']:
                self.showError("Please verify your email before logging in!")
                return

            self.userID = user['localId']
            welcome_screen = WelcomeScreen(self.userID)
            widget.addWidget(welcome_screen)
            widget.setCurrentWidget(welcome_screen)
            self.email.clear()
            self.password.clear()
        except Exception as e:
            self.showError(f"Invalid Email or Password! {str(e)}")
            self.password.clear()
            
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

    def ForgetPassword(self):
        email, ok = QInputDialog.getText(self, 'Reset Password', 'Enter your email:')
        if ok and email:
            try:
                authfire.send_password_reset_email(email)
                QMessageBox.information(self, 'Success', 'Password reset email sent!')
            except Exception:
                self.showError("Error: Invalid Email")
    
    def focusPassword(self):
        self.password.setFocus()


# --------------------- Sign Up Window ---------------------
class CreateAcc(QMainWindow):
    def __init__(self):
        super(CreateAcc, self).__init__()
        self.setWindowTitle("Habit Tracker")
        uic.loadUi(os.path.join(os.path.dirname(__file__), "SignUp.ui"), self)
        self.setStyleSheet(HONEYCOMB_STYLESHEET)

        self.name.setPlaceholderText("Your Name")
        self.email.setPlaceholderText("Your Email")
        self.password.setPlaceholderText("Create a Password")
        self.confirmPassword.setPlaceholderText("Confirm Password")

        self.password.setEchoMode(QLineEdit.Password)
        self.confirmPassword.setEchoMode(QLineEdit.Password)
        self.signupbutton.clicked.connect(self.createAccountFunction)
        self.backToLogin.clicked.connect(self.go_back_to_login)

        self.name.returnPressed.connect(self.focusEmail)
        self.email.returnPressed.connect(self.focusPassword)
        self.password.returnPressed.connect(self.focusConfirmPassword)
        self.confirmPassword.returnPressed.connect(self.createAccountFunction)

    def createAccountFunction(self):
        email = self.email.text()
        password = self.password.text()
        confirm_password = self.confirmPassword.text()
        name = self.name.text()
        
        if not email or not password or not confirm_password or not name:
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
            self.add_username(databases, userID, name)
            authfire.send_email_verification(user['idToken'])
            QMessageBox.information(self, 'Verification Sent', 'Please check your email to verify your account!')
            widget.setCurrentIndex(0)
            self.email.clear()
            self.password.clear()
            self.confirmPassword.clear()
            self.name.clear()
        except Exception as e:
            self.showError("Account creation failed. Try again.")
            print(e)
        
    def showError(self, message):
        error = QMessageBox()
        error.setIcon(QMessageBox.Warning)
        error.setText(message)
        error.setWindowTitle("Signup Error")
        error.exec_()

    def add_username(self, db, UUID, name):
        db.child(UUID).child("name").set(name)

    def go_back_to_login(self):
        widget.setCurrentIndex(0)
        self.email.clear()
        self.password.clear()
        self.confirmPassword.clear()
        self.name.clear()
    
    def focusEmail(self):
        self.email.setFocus()
    
    def focusPassword(self):
        self.password.setFocus()
    
    def focusConfirmPassword(self):
        self.confirmPassword.setFocus()


# --------------------- WelcomeScreen Window ---------------------
class WelcomeScreen(QMainWindow):
    def __init__(self,userID):
        super(WelcomeScreen, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "WelcomeScreen.ui"), self)
        self.setWindowTitle("Habit Tracker")
        self.userID = userID
        username = databases.child(userID).child("name").get()
        name = username.val()
        self.Quote.setStyleSheet(
            """QLabel{
            font-size: 16px;
            }"""
        )

        # Apply the background and text styles for the entire window
        self.setStyleSheet(HONEYCOMB_STYLESHEET)
        self.Quote.setText(selected_quote)
        self.QuoteOwner.setText(name)
        
        
         

        # Connections
        self.AddHabit.clicked.connect(self.on_add_habit)
        self.DeleteHabit.clicked.connect(self.on_delete_habit)
        self.LogOut.clicked.connect(self.BackToLogin)
        self.ViewHabit.clicked.connect(self.view_habits) 
        self.SendQuote.clicked.connect(self.quote_sharing)
        self.Streaks.clicked.connect(self.show_streaks)

        


    def on_add_habit(self):
        self.add_habit = AddHabit(self.userID)
        self.add_habit.show()
    
    def quote_sharing(self):
        quote_sharing = QuoteSharing(self.userID)
        quote_sharing.exec_()

    def view_habits(self):
        self.view_habits_window = ViewHabitScreen(self.userID)
        self.view_habits_window.exec_()
        

    def on_delete_habit(self):
        self.delete_habit = DeleteHabit(self.userID)
        self.delete_habit.exec_()

    def BackToLogin(self):
        widget.setCurrentIndex(0)

    def show_streaks(self):
        """Create and show the Streak dialog."""
        self.streak_dialog = Streak(self.userID, self) 
        self.hide()
        self.streak_dialog.exec_()
        self.show()
        

# --------------------- ViewHabit Screen -------------------- 
class ViewHabitScreen(QDialog):
    def __init__(self, userID):
        super(ViewHabitScreen, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "ViewHabit.ui"), self)
        self.setWindowIcon(QtGui.QIcon("logo.jpg"))
        self.userID = userID 

        # Set up UI elements
        self.setStyleSheet(HONEYCOMB_STYLESHEET)
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
        self.setWindowIcon(QtGui.QIcon("logo.jpg"))
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
            streak_data = databases.child(self.userID).child("habits").get()
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

        self.setStyleSheet(HONEYCOMB_STYLESHEET)

        self.userID = userID
        self.streak_dialog = streak_dialog

        # Correctly find the QListWidget
        self.habit_list = self.findChild(QListWidget, "habit_list")

        # Buttons
        self.addStreak = self.findChild(QPushButton, "addStreak")
        self.addStreak.clicked.connect(self.on_add_streak)

        self.backToStreaks = self.findChild(QPushButton, "backToStreaks")
        self.backToStreaks.clicked.connect(self.close)

        self.load_habits()

    def load_habits(self):
        self.habit_list.clear()
        try:
            habits = databases.child(self.userID).child("habits").get()
            if habits.each():
                for habit in habits.each():
                    habit_data = habit.val()
                    habit_id = habit.key()
                    streak_counter = habit_data.get("streakCounter", 0)

                    habit_text = f"{habit_data['title']} - {habit_data['start_date']} ({habit_data['difficulty']}) | Streak: {streak_counter}"
                    item = QListWidgetItem(habit_text)
                    item.setCheckState(Qt.Unchecked)
                    item.setData(Qt.UserRole, habit_id)
                    self.habit_list.addItem(item)
            else:
                self.habit_list.addItem("No habits found.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load habits: {str(e)}")

    def on_add_streak(self):
        try:
            updated_any = False
            for index in range(self.habit_list.count()):
                item = self.habit_list.item(index)
                if item.checkState() == Qt.Checked:
                    habit_id = item.data(Qt.UserRole)
                    if habit_id:
                        self.update_streak_for_habit(habit_id)
                        updated_any = True

            if updated_any:
                QMessageBox.information(self, "Success", "Streaks updated for all checked habits!")
                self.load_habits()  # Refresh list with updated streaks
            else:
                QMessageBox.information(self, "Notice", "No habits were selected.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update streaks: {str(e)}")

    def update_streak_for_habit(self, habit_id):
        try:
            habit_ref = databases.child(self.userID).child("habits").child(habit_id)
            habit_data = habit_ref.get().val()

            current_time = datetime.datetime.now()
            streak_counter = habit_data.get("streakCounter")
            last_checked_time = habit_data.get("lastCheckedTime")
            print(last_checked_time)
            last_checked = datetime.datetime.fromisoformat(last_checked_time)

            if last_checked_time:
                last_checked = datetime.datetime.fromisoformat(last_checked_time)
                time_diff = (current_time - last_checked).total_seconds()
                print(time_diff)

                if time_diff >= 86400:  # Less than 24 hours
                    streak_counter += 1
                    databases.child(self.userID).child("habits").child(habit_id).update({"lastCheckedTime": datetime.datetime.now().isoformat()})
                    databases.child(self.userID).child("habits").child(habit_id).update({"streakCounter": streak_counter})
                    print(f"step 1",streak_counter)
                else:
                    QMessageBox.critical(self,"Error","24 hours have not passed")

            # Optional: Refresh streak display in the main streak dialog
            self.streak_dialog.load_streak_counter()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update streak for habit {habit_id}: {str(e)}")


# --------------------- Sharing quotes button  -------------------- 
class QuoteSharing(QDialog):

    def __init__(self, userID):
        super(QuoteSharing, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "QuoteSharing.ui"), self)
        self.setWindowIcon(QtGui.QIcon("logo.jpg"))
        self.setStyleSheet(HONEYCOMB_STYLESHEET)
        self.userID = userID
        
        self.submitButton.clicked.connect(self.submit_quote)

    def submit_quote(self):

        username = databases.child(self.userID).child("name").get().val()

        quote_text = self.Quote.toPlainText().strip()

        if not quote_text:
            QMessageBox.warning(self, "Error", "Please enter a quote before submitting.")
            return
        
        
        prompt = f"Does this quote look appropriate for public view? Reply with only 'true' or 'false': {quote_text}"
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        
        if not response or not hasattr(response, "text"):
            QMessageBox.critical(self, "Error", "Failed to verify quote with AI moderation.")
            return

        ai_decision = response.text.strip().lower()
        
        if ai_decision == "true":
            try:
                databases.child("UserQuotes").push({username: quote_text})
                QMessageBox.information(self, "Success", "Your quote has been submitted!")
                self.Quote.clear()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to submit quote: {str(e)}")
        else:
            QMessageBox.warning(self, "Rejected", "Your quote was deemed inappropriate for public view.")


# --------------------- AddHabit Dialogue --------------------

class AddHabit(QDialog):
    
    close_dialog_signal = pyqtSignal()

    def __init__(self,userID):
        super(AddHabit, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "AddHabit.ui"), self)
        self.setWindowIcon(QtGui.QIcon("logo.jpg"))
        self.userID = userID # add userID

        # Connect the signal to the accept() method
        self.close_dialog_signal.connect(self.accept)

        # Set background color and text color
        self.setStyleSheet(HONEYCOMB_STYLESHEET)
            

        # Set the style for the Save and Cancel buttons
        save_button = self.CancelSaveBox.button(QDialogButtonBox.Save)
        cancel_button = self.CancelSaveBox.button(QDialogButtonBox.Cancel)

        

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
            "difficulty": difficulty,
            "lastCheckedTime": datetime.datetime.now().isoformat(),
            "streakCounter": 0
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
        self.setWindowIcon(QtGui.QIcon("logo.jpg"))
        self.userID = userID #add user ID
        # Set styles
        self.setStyleSheet(HONEYCOMB_STYLESHEET)

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
                    self.habit_list.addItem(item)  
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

myappid = 'mycompany.myapp.habittracker'  # Unique ID for your app
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

app = QApplication(sys.argv)

# Set the icon BEFORE creating any widgets
icon_path = "logo.ico"
app.setWindowIcon(QtGui.QIcon(icon_path))  # This ensures the taskbar icon appears

widget = QStackedWidget()
mainWindow = Login()
createAccountWindow = CreateAcc()

widget.addWidget(mainWindow)
widget.addWidget(createAccountWindow)

widget.setWindowTitle("Habit Tracker")
widget.setWindowIcon(QtGui.QIcon(icon_path))  # Ensures the window also has the icon
widget.setFixedHeight(650)
widget.setFixedWidth(650)
#widget.showFullScreen()
widget.show()

sys.exit(app.exec_())