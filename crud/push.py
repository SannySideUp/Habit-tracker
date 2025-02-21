import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyrebase
from utils.config import firebaseConfig
from utils.generateID import generateRandomUserID
#copy original config and modify the url
def userDB(userPath):
    firebaseConfigHabit = {}
    for key,value in firebaseConfig.items():
        if key == "databaseURL":
            firebaseConfigHabit[key] = value+userPath
            print(value+userPath)
        else:
            firebaseConfigHabit[key] = value
    return firebaseConfigHabit

def makeNewPath(path):
    config = userDB(path)
    firebase = pyrebase.initialize_app(config)
    return firebase.database() 

userPath = "-OJTQx0MIMXm4z5DeAF8"
userPath1="/habits/"
db = makeNewPath(userPath1)

def push(db): #will generate a random id in the database
    db.push({"key": "value"})

def appendToUser(db,key, value):
    db.child(key).set(value)
##
def appendNewUser(db,UUID, key,value):
    db.child(UUID).child(key).set(value)

usersDb = makeNewPath("")
#push(usersDb)
def createNewUser(db,email,password):
    UUID = generateRandomUserID()
    appendNewUser(db, "users", UUID, email)
email = "fake@gmail.com"
password = "fakepassword"
UUID = generateRandomUserID()
appendNewUser(usersDb, "users",UUID, "anotherfake@gmail.com")
#createNewUser(usersDb,email,password)
#appendToUser(usersDb, "users",generateRandomUserID())