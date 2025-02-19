import pyrebase
from utils.config import firebaseConfig

#copy original config and modify the url
firebaseConfigHabit = {}
for key,value in firebaseConfig.items():
    print(key,value)
    if key == "databaseURL":
        firebaseConfigHabit[key] = value+"habits/"
        print(firebaseConfigHabit[key])
    else:
        firebaseConfigHabit[key] = value

firebase = pyrebase.initialize_app(firebaseConfigHabit)
db = firebase.database() 

def createNewUserID(db):
    db.push({"text": "", "user_id":"test"})

createNewUserID(db)