from bs4 import BeautifulSoup

import pyrebase
# configure and connect with firebase
config = {
    "apiKey": "AIzaSyCsvb2hDlh-1xJ8V8ZR2DDWdo9HPaS6X80",
    "authDomain": "whine-and-cheese.firebaseapp.com",
    "databaseURL": "https://whine-and-cheese.firebaseio.com",
    "storageBucket": "whine-and-cheese.appspot.com",
    "serviceAccount": "whine-and-cheese-firebase-adminsdk-45d47-21edf278e4.json"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

def addWineAndCheese(wine, cheese):
    path = "wines/" + wine
    keys = db.child(path).shallow().get().val()

    # if wine is in database
    if (keys):
        all_cheese = db.child(path).get()
        # return if cheese is already mapped to wine
        for DBCheese in all_cheese.each():
            if (str(DBCheese.val()).__eq__(cheese)):
                return
        # otherwise add cheese with unique numerical key
        key =(len(keys)+1)
        path = "wines/" + wine + "/" + str(key)
        db.child(path).set(cheese)
    else:
        # add 1 as the first cheese key
        data = {"1": cheese}
        db.child(path).set(data)

# actual parsing of cheese file
soup = BeautifulSoup(open("somecheese.html"),"html.parser")
text = soup.get_text().lower()
text = text.split('\n')
text = list(filter(None, text))
for i in range(0, (len(text)-1), 2):
    addWineAndCheese(text[i+1], text[i])