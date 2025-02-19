import pyrebase
from push import userDB

firebaseConfig = userDB("/")
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database() 

tmp = db.get()
print(tmp.val())

