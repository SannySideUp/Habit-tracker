import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyrebase
from utils.config import firebaseConfig
from utils.generateID import generateRandomUserID
#copy original config and modify the url
def userDB(user_path,firebase_config):
    firebase_config_habit = {}
    for key,value in firebase_config.items():
        if key == "databaseURL":
            firebase_config_habit[key] = value+user_path
        else:
            firebase_config_habit[key] = value
    return firebase_config_habit

def makeNewPath(path,firebase_config):
    config = userDB(path,firebase_config)
    firebase = pyrebase.initialize_app(config)
    return firebase.database() 

userPath = "-OJTQx0MIMXm4z5DeAF8"
userPath1="/habits/"
db = makeNewPath(userPath1,firebaseConfig)

def push(db): #will generate a random id in the database
    db.push({"key": "value"})

def appendToUser(db,key, value):
    db.child(key).set(value)
##
def appendNewUser(db,UUID, key,value):
    db.child(UUID).child(key).set(value)

usersDb = makeNewPath("",firebaseConfig)
#push(usersDb)
def createNewUser(db,email,password):
    UUID = generateRandomUserID()
    appendNewUser(db, "users", UUID, email)
email = "fake@gmail.com"
password = "fakepassword"
UUID = generateRandomUserID()
#appendNewUser(usersDb, "users",UUID, "anotherfake@gmail.com")
#createNewUser(usersDb,email,password)
#appendToUser(usersDb, "users",generateRandomUserID())

def addHabits(path,firebase_config,data):
    db = makeNewPath(path,firebase_config)
    db.push(data)

def create_new_user_in_users(path,firebase_config, UUID, key, value):
    db = makeNewPath(path,firebase_config)
    db.child(UUID).child(key).set(value)

def create_new_user_in_habits( db, UUID,data):
    db.child("habits").child(UUID).set(data)