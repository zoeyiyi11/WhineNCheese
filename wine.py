import pickle as pkl
import difflib
import re
import nltk.sentiment.vader as vader


d = difflib.Differ()
analyzer = vader.SentimentIntensityAnalyzer()

winez = pkl.load(open("wines.pkl", "rb"))
def parseWine(inp):
	inpt =inp.lower()
	neg = analyzer.polarity_scores(inpt)['neg']
	pos = analyser.polarity_scores(inpt)['pos']
	matched = False
	for wine in winez:
		if(matched == False):
			wine = wine.lower()
			if (re.search(wine, inpt)):
				matched = True
				print(wine)
			d = difflib.SequenceMatcher(None,wine, inpt).ratio()
			if d > 0.6:
				matched = True
				print(wine)
		return {"string": inp, "wine": matched, "negative_sentiment": neg,"positive_sentiment": pos}