import pyrebase
import re
import regex
import difflib
import random

config = {
    "apiKey": "AIzaSyCsvb2hDlh-1xJ8V8ZR2DDWdo9HPaS6X80",
    "authDomain": "whine-and-cheese.firebaseapp.com",
    "databaseURL": "https://whine-and-cheese.firebaseio.com",
    "storageBucket": "whine-and-cheese.appspot.com",
    "serviceAccount": "whine-and-cheese-firebase-adminsdk-45d47-21edf278e4.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def getResponse(wine, threshold = 0.7):
	## if it's a wine, get a cheese
	if wine["type"] == "wine":
		wine_json = dict(db.child('wines').get().val())
		wines = [w for w in wine_json]
		### currently doesn't check on misspelled types
		red = (True if re.search('(^|\W)red($|\W)', wine["string"], re.IGNORECASE) else False)
		white = (True if re.search('(^|\W)white($|\W)', wine["string"], re.IGNORECASE) else False)
		dessert = (True if re.search('(^|\W)dessert($|\W)', wine["string"], re.IGNORECASE) else False)
		try:
			result_wine = difflib.get_close_matches(wine, wines, cutoff=threshold)[0]
		except:
			result_wine = random.choice([w for w in wine_json if ((wine_json[w]["type"] == "red") if red else False) or ((wine_json[w]["type"] == "white") if white else False) or ((wine_json[w]["type"] == "dessert") if dessert else False) or (not white and not red and not dessert)])
		result_cheese = random.choice(wine_json[result_wine]["cheeses"])
		return {"type": "wine", "wine": result_wine, "cheese": result_cheese}
	else:
		lines = db.child('lines').get().val()
		result_line = random.choice(lines)
		return {"type": "whine",  "response": result_line}
