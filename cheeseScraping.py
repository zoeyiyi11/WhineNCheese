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


def addToDatabaseArray(path, value):
    keys = db.child(path).shallow().get().val()
    # if key has a mapped value already, add to the array
    if (keys):
        all_vals = db.child(path).get()
        # return if value is already in database
        for DBCheese in all_vals.each():
            if (str(DBCheese.val()).__eq__(value)):
                return
        # otherwise add value at next index of array
        index = len(keys)
        path = path + "/" + str(index)
        db.child(path).set(value)
    else:
        # add first element of array (index 0)
        data = {"0":value}
        db.child(path).set(data)

def addCheesyResponse(soCheesy):
    path = "cheesyResponses"
    keys = db.child(path).shallow().get().val()
    index = len(keys)
    path = path + "/" + str(index)
    db.child(path).set(soCheesy)

def addWineAndCheese(wine, cheese):
    path = "wines/" + wine + "/cheeses"
    addToDatabaseArray(path, cheese)
    path = "wines/" + wine + "/type"
    wine_type = db.child(path).shallow().get().val()
    if (not wine_type):
        db.child(path).set("")


# # actual parsing of cheese file
# soup = BeautifulSoup(open("somecheese.html"),"html.parser")
# text = soup.get_text().lower()
# text = text.split('\n')
# text = list(filter(None, text))
# for i in range(0, (len(text)-1), 2):
#     addWineAndCheese(text[i+1], text[i])