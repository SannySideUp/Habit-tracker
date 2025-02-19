import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyrebase
from utils.config import firebaseConfig
#copy original config and modify the url
def userDB(userPath):
    firebaseConfigHabit = {}
    for key,value in firebaseConfig.items():
        if key == "databaseURL":
            firebaseConfigHabit[key] = value+"/habits/"+userPath
        else:
            firebaseConfigHabit[key] = value
    return firebaseConfigHabit
userPath = "-OJTQx0MIMXm4z5DeAF8"
firebaseConfigHabit = userDB(userPath)
firebase = pyrebase.initialize_app(firebaseConfigHabit)
db = firebase.database() 


def createNewUserID(db):
    db.push({"uniqueUserID": 1234})

def appendToUser(db,key, value):
    db.child(key).set(value)
appendToUser(db, "NewKey","NewValue")