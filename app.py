from flask import Flask


# Create Flask's `app` object
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"