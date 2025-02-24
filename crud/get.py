import pyrebase
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crud.push import makeNewPath

""" firebaseConfig = userDB("/")
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database() 

tmp = db.get()
print(tmp.val()) """

def getUserDetails(user_path,firebase_config):
    db = makeNewPath(user_path,firebase_config)
    return db.get().val()


