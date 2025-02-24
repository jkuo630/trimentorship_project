from flask import Flask, jsonify, request
from flask_cors import CORS

# Create Flask's `app` object
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# structure of session 
session = {
    'topic': str,
    'time': int,
    'app': str,
    'status': bool,
}

@app.route("/")
def hello():
    return "Hello World!"

# user config endpoint - post
# anthony 
# make a local array to temp store things 
# we want this endpoint to be able to add new users and their info to this local array 
# we want to return, the full list of users 
@app.route("/userconfig")
def temp():
    return "Hello World!"

# register callback endpoint - post 
# jason
@app.route("/registercallback")
def temp():
    return "Hello World!"

# startSession endpoint - post
# jason
@app.route("/start")
def temp():
    return "Hello World!"

# endSession endpoint - post
# anthony 
# update data and turn status into False
# return that session 
@app.route("/end")
def temp():
    return "Hello World!"

# currentSession endpoint - get 
# anthony 
# make a temp session array/json structure where we store all the sessions 
# return the session that is currently active 
@app.route("/current")
def temp():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True, port=5001)