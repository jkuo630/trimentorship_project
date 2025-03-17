from flask import Flask, jsonify, request
from flask_cors import CORS
import MySQLdb

from gender import Gender

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

mydb = MySQLdb.connect(host="localhost", user="root", password = "my_password", database = "interrupt_data")
# user should enter their own password

mycursor = mydb.cursor()

# user config endpoint - post
# anthony 
# make a local array to temp store things 
# we want this endpoint to be able to add new users and their info to this local array 
# we want to return, the full list of users 
@app.route("/create_user", methods = ['POST'])
def add_user():
    global mycursor

    data = request.get_json()

    mycursor.execute("select max(user_id) from users")
    max_user_id = mycursor.fetchone()[0]
    if (max_user_id == None):
        max_user_id = 0
    new_id = max_user_id + 1

    query = ("insert into users values(%s, %s, %s, %s, %s)")
    mycursor.execute(query, (new_id, data["email"], data["gender"], data["country"], data["school"]))
    return jsonify({"message": "User created", "user_id": new_id, "users": get_users_as_dict()}), 201

# get all users
@app.route("/get_users", methods = ['GET'])
def get_users():
    return jsonify(get_users_as_dict())

def get_users_as_dict():
    global mycursor
    mycursor.execute("select * from users")
    rows = mycursor.fetchall()
    column_names = [description[0] for description in mycursor.description]
    users = [dict(zip(column_names, row)) for row in rows]
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
    global mycursor

    data = request.get_json()
    mycursor.execute("select max(session_id) from sessions")
    max_session_id = mycursor.fetchone()[0]
    if (max_session_id == None):
        max_session_id = 0
    new_id = max_session_id + 1

    query = ("insert into sessions values(%s, %s, %s, %s, %s, %s)")
    mycursor.execute(query, (new_id, data["user_id"], data["topic"], data["time"], data["app"], data["status"]))
    return jsonify({"message": "Session created", "session_id": new_id, "sessions": get_sessions_as_dict()}), 201

# start_session endpoint - update
# jason
# pass in an id, set status to True 
@app.route("/start_session", methods=["POST"])
def start_session():
    global mycursor

    data = request.get_json()
    session_id = data.get("session_id")

    mycursor.execute("select * from sessions where session_id = %s", (session_id,))
    session_to_start = mycursor.fetchone()
    if (session_to_start == None):
        return jsonify({"error": "Session not found", "sessions": get_sessions_as_dict()}), 404
    query = ("update sessions set status = true where session_id = %s")
    mycursor.execute(query, (session_id,))
    return jsonify({"message": f"Session {session_id} started", "status": True}), 200
    

# delete_session endpoint - POST 
# anthony 
# pass in an id, check if it exists, then remove it 
@app.route("/delete_session", methods=["POST"])
def delete_session():
    global mycursor

    data = request.get_json()
    session_id = data.get("session_id")

    mycursor.execute("select * from sessions where session_id = %s", (session_id,))
    session_to_delete = mycursor.fetchone()
    if (session_to_delete == None):
        return jsonify({"error": "Session not found"}), 404
    query = ("delete from sessions where session_id = %s")
    mycursor.execute(query, (session_id,))

    return jsonify({"message": f"Session {session_id} deleted"}), 200

# end_session endpoint - POST
# anthony 
# update data and turn status into False
# return that session 
@app.route("/end_session", methods = ["POST"])
def end_session():
    global mycursor

    data = request.get_json()
    session_id = data.get("session_id")

    mycursor.execute("select * from sessions where session_id = %s", (session_id,))
    session_to_end = mycursor.fetchone()
    if (session_to_end == None):
        return jsonify({"error": "Session not found", "sessions": get_sessions_as_dict()}), 404
    query = ("update sessions set status = false where session_id = %s")
    mycursor.execute(query, (session_id,))
    return jsonify({"message": f"Session {session_id} ended", "status": False}), 200

# get_current_session endpoint - get 
# anthony 
# make a temp session array/json structure where we store all the sessions 
# return the session that is currently active 
@app.route("/current", methods = ['GET'])
def get_current_session():
    global mycursor
    mycursor.execute("select * from sessions where status = true")
    rows = mycursor.fetchall()
    column_names = [description[0] for description in mycursor.description]
    active_sessions = [dict(zip(column_names, row)) for row in rows]
    
    if active_sessions:
        return jsonify({"active_sessions": active_sessions}), 200
    return jsonify({"message": "No active sessions"}), 404

# get all sessions
@app.route("/get_sessions", methods = ['GET'])
def get_sessions():
    return jsonify(get_sessions_as_dict())

def get_sessions_as_dict():
    global mycursor
    mycursor.execute("select * from sessions")
    rows = mycursor.fetchall()
    column_names = [description[0] for description in mycursor.description]
    sessions = [dict(zip(column_names, row)) for row in rows]
    return sessions

if __name__ == '__main__':
    app.run(debug=True, port=5001) 