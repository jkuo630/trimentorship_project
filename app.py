from flask import Flask, jsonify, request
from flask_cors import CORS

# Create Flask's `app` object
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# structure of session 
sessions = [
    {"topic": "CPSC 121", "time": 50, "app": "SmartPomodoro", "status": False},
    {"topic": "DSCI 100", "time": 20, "app": "SmartPomodoro", "status": True},
    {"topic": "Afternoon nap", "time": 90, "app": "SmartAlarm", "status": False},
]

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
@app.route("/registercallback", methods=["POST"])
def register_callback():
    return jsonify({"message": "Callback registered"}), 200

# startSession endpoint - post
# jason
# instantiate a new session object, set it to true, making sure its the only true 
@app.route("/start")
def start_session():
    global sessions
    data = request.json
    topic = data.get("topic")

    session = next((s for s in sessions if s["topic"] == topic), None)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    active_session = get_active_session()
    if active_session:
        return jsonify({"error": f"Another session ('{active_session['topic']}') is already active"}), 400

    session["status"] = True
    return jsonify({"message": f"Session '{topic}' started"}), 20

# help function to ensure a session is the only one set to true -> singleton instance 
def get_active_session():
    return next((session for session in sessions if session["status"]), None)

# endSession endpoint - post
# anthony 
# update data and turn status into False
# return that session 

@app.route("/end", methods = ['UPDATE'])
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