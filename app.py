from flask import Flask, jsonify, request
from flask_cors import CORS

from gender import Gender

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

users = {
    1: {"email": "12345678@gmail.com", "gender": Gender.FEMALE.name, "country": "Andorra", "school": "University of Andorra"},
    2: {"email": "anemail@gmail.com", "gender": Gender.MALE.name, "country": "Japan", "school": "University of Tokyo"},
    3: {"email": "anotheremail@hotmail.com", "gender": Gender.MALE.name, "country": "Australia", "school": "University of Melbourne"}
}

sessions = {
    1: {
        "user-id": 1,
        "topic": 'CPSC 121',
        "time": 50,
        "app": "SmartPomodoro",
        "status": False
    },
    2: {
        "user-id": 2,
        "topic": 'DSCI 100',
        "time": 20,
        "app": "SmartPomodoro",
        "status": True
    },
    3: {
        "user-id": 2,
        "topic": "Afternoon nap",
        "time": 90,
        "app": "SmartAlarm",
        "status": False
    }
}

# user config endpoint - post
# anthony 
# make a local array to temp store things 
# we want this endpoint to be able to add new users and their info to this local array 
# we want to return, the full list of users 
@app.route("/create_user", methods = ['POST'])
def add_user():
    data = request.get_json()
    new_id = max(users.keys(), default=0) + 1  # Generate unique user ID

    users[new_id] = {
        "email": data["email"],
        "gender": data["gender"],
        "country": data["country"],
        "school": data["school"]
    }

    return jsonify({"message": "User created", "user_id": new_id, "users": users}), 201

# get all users
@app.route("/get_users", methods = ['GET'])
def get_users():
    return users

# register callback endpoint - post 
# jason
@app.route("/registercallback", methods=["POST"])
def register_callback():
    return jsonify({"message": "Callback registered"}), 200


# create_session endpoint - post
# jason
# pass in a session object
@app.route("/create_session", methods=["POST"])
def create_session():
    data = request.get_json()
    new_id = max(sessions.keys(), default=0) + 1

    sessions[new_id] = {
        "user-id": data["user-id"],
        "topic": data["topic"],
        "time": data["time"],
        "app": data["app"],
        "status": data["status"]
    }

    return jsonify({"message": "Session created", "session_id": new_id, "sessions": sessions}), 201

# start_session endpoint - update
# jason
# pass in an id, set status to True 
@app.route("/start_session", methods=["POST"])
def start_session():
    data = request.get_json()
    session_id = data.get("session_id")

    if sessions[session_id]:
        sessions[session_id]["status"] = True
        return jsonify({"message": f"Session {session_id} started", "status": True}), 200
    return jsonify({"error": "Session not found", "sessions": sessions}), 404

# delete_session endpoint - POST 
# anthony 
# pass in an id, check if it exists, then remove it 
@app.route("/delete_session", methods=["POST"])
def delete_session():
    data = request.get_json()
    session_id = data.get("session_id")

    if sessions[session_id]:
        del sessions[session_id]
        return jsonify({"message": f"Session {session_id} deleted"}), 200
        
    return jsonify({"error": "Session not found"}), 404

# end_session endpoint - POST
# anthony 
# update data and turn status into False
# return that session 
@app.route("/end_session", methods = ["POST"])
def end_session():
    data = request.get_json()
    session_id = data.get("session_id")

    if sessions[session_id]:
        sessions[session_id]["status"] = False
        return jsonify({"message": f"Session {session_id} ended", "status": False}), 200
    return jsonify({"error": "Session not found", "sessions": sessions}), 404

# get_current_session endpoint - get 
# anthony 
# make a temp session array/json structure where we store all the sessions 
# return the session that is currently active 
@app.route("/current", methods = ['GET'])
def get_current_session():
    active_sessions = [session for session in sessions.values() if session["status"]]
    
    if active_sessions:
        return jsonify({"active_sessions": active_sessions}), 200
    return jsonify({"message": "No active sessions"}), 404

# get all sessions
@app.route("/get_sessions", methods = ['GET'])
def get_sessions():
    return sessions

if __name__ == '__main__':
    app.run(debug=True, port=5001)