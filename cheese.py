from flask import Blueprint, jsonify, request

import pickle as pkl
import difflib
import re
import random
import pyrebase
import nltk.sentiment.vader as vader
from nltk import ngrams

cheese = Blueprint('cheese', __name__, template_folder='templates')

d = difflib.Differ()
analyzer = vader.SentimentIntensityAnalyzer()

config = {
    "apiKey": "AIzaSyCsvb2hDlh-1xJ8V8ZR2DDWdo9HPaS6X80",
    "authDomain": "whine-and-cheese.firebaseapp.com",
    "databaseURL": "https://whine-and-cheese.firebaseio.com",
    "storageBucket": "whine-and-cheese.appspot.com",
    "serviceAccount": "whine-and-cheese-firebase-adminsdk-45d47-21edf278e4.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

winez = pkl.load(open("wines.pkl", "rb"))

def getResponse(query, threshold = 0.7, neg_threshold=0.3):
	## if it's a wine, get a cheese
	inp = parseWine(query)
	print(inp)
	result_wine = ""
	unsure = False
	if inp["wine"]:
		wine_json = dict(db.child('wines').get().val())
		wines = [w for w in wine_json]

		red = (True if re.search('(^|\W)red($|\W)', inp["string"], re.IGNORECASE) else False)
		white = (True if re.search('(^|\W)white($|\W)', inp["string"], re.IGNORECASE) else False)
		dessert = (True if re.search('(^|\W)dessert($|\W)', inp["string"], re.IGNORECASE) else False)

		# check if wine perfect substring/equal in input
		matched = False
		for wine in wines:
			if re.search(wine.lower(), inp["string"]):
				result_wine = wine
				matched = True

		# check if wine above threshold substring in input 
		if not matched:
			words = inp["string"].split()
			for n in range(1, 4):
				grams = [" ".join(words[i:i+n]) for i in range(0, len(words), n)]
				for g in grams:
					try:
						result_wine = difflib.get_close_matches(g, wines, cutoff=threshold)[0]
						matched = True
					except:
						continue
					if matched:
						break

		# check if wine above threshold to input
		if not matched:
			try:
				result_wine = difflib.get_close_matches(inp["strings"], wines, cutoff=threshold)[0]
			except:
				unsure = True
				result_wine = random.choice([w for w in wine_json if ((wine_json[w]["type"] == "red") if red else False) or ((wine_json[w]["type"] == "white") if white else False) or ((wine_json[w]["type"] == "dessert") if dessert else False) or (not white and not red and not dessert)])
		
		result_cheese = random.choice(wine_json[result_wine]["cheeses"])
	else:
		result_cheese = ""

	if inp["negative_sentiment"] >= neg_threshold:
		lines = db.child('cheesyResponses').get().val()
		result_line = random.choice(lines)
	else:
		result_line = ""

	if inp["negative_sentiment"] > 0.6:
		mood = "sad"
	elif inp["wine"]:
		mood = "helping"
	else:
		mood = "happy"
	return {"line": result_line, "cheese": result_cheese, "wine": result_wine, "mood": mood, "unsure": unsure}

def parseWine(inp, threshold=0.7):
	inpt = inp.lower()
	neg = analyzer.polarity_scores(inpt)['neg']
	pos = analyzer.polarity_scores(inpt)['pos']
	matched = False
	words = inpt.split()

	for wine in winez:
		if(matched == False):
			wine = wine.lower()
			if (re.search(wine, inpt)):
				matched = True
			if not matched:
				for n in range(1, 4):
					grams = [" ".join(words[i:i+n]) for i in range(0, len(words), n)]
					try:
						result_wine = difflib.get_close_matches(wine, grams, cutoff=threshold)[0]
						matched = True
					except:
						continue
					if matched:
						break
			d = difflib.SequenceMatcher(None, wine, inpt).ratio()
			if d > threshold:
				matched = True
	return {"string": inpt, "wine": matched, "negative_sentiment": neg,"positive_sentiment": pos}

@cheese.route("/process", methods=["POST"])
def process():
	try:
	    query = request.get_json()["query"]
	    result = getResponse(query)
	    return jsonify(result), 200
	except Exception as e:
		print(e)
		return jsonify({"error": "There was an error."}), 400
