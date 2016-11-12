from bs4 import BeautifulSoup

import pyrebase
config = {
    "apiKey": "AIzaSyCsvb2hDlh-1xJ8V8ZR2DDWdo9HPaS6X80",
    "authDomain": "whine-and-cheese.firebaseapp.com",
    "databaseURL": "https://whine-and-cheese.firebaseio.com",
    "storageBucket": "whine-and-cheese.appspot.com",
    "serviceAccount": "whine-and-cheese-firebase-adminsdk-45d47-21edf278e4.json"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

soup = BeautifulSoup(open("somecheese.html"),"html.parser")
text = soup.get_text().lower()#.split()
text = text.split('\n')
text = list(filter(None, text)) # fastest

def addWineAndCheese(wine, cheese):
    path = "wines/" + wine
    keys = db.child(path).shallow().get().val()

    if (keys):
        all_cheese = db.child(path).get()
        for DBCheese in all_cheese.each():
            if (str(DBCheese.val()).__eq__(cheese)):
                return
        key =(len(keys)+1)
        path = "wines/" + wine + "/" + str(key)
        db.child(path).set(cheese)
    else:
        data = {"1": cheese}
        db.child(path).set(data)


for i in range(0, (len(text)-1), 2):
    addWineAndCheese(text[i+1], text[i])