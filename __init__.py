from flask import Flask, render_template, jsonify, Blueprint
from cheese import *

app = Flask(__name__)
app.register_blueprint(cheese)

@app.route("/")
def init():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()