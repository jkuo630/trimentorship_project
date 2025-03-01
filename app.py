from flask import Flask, jsonify, request
from flask_cors import CORS

from gender import Gender

# Create Flask's `app` object
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# structure of user
user = {
    'email': str,
    'gender': Gender,
    'country': str,
    'school': bool,
}

# structure of session 
session = {
    'topic': str,
    'time': int,
    'app': str,
    'status': bool,
}

users = [
    {
        "user-id": 1,
        "email": "12345678@gmail.com",
        "gender": Gender.FEMALE.name,
        "country": "Andorra",
        "school": "University of Andorra"
    },
    {
        "user-id": 2,
        "email": "anemail@gmail.com",
        "gender": Gender.MALE.name,
        "country": "Japan",
        "school": "University of Tokyo" 
    },
    {
        "user-id": 3,
        "email": "anotheremail@hotmail.com",
        "gender": Gender.MALE.name,
        "country": "Australia",
        "school": "University of Melbourne" 
    }
]

sessions = [
    {
        'user-id': 1,
        'topic': 'CPSC 121',
        'time': 50,
        'app': "SmartPomodoro",
        'status': False
    },
    {
        'user-id': 2,
        'topic': 'DSCI 100',
        'time': 20,
        'app': "SmartPomodoro",
        "status": True,
    },
    {
        'user-id': 2,
        'topic': "Afternoon nap",
        'time': 90,
        "app": "SmartAlarm",
        "status": False
    }
]

@app.route("/")
def hello():
    return "Hello World!"

# user config endpoint - post
# anthony 
# make a local array to temp store things 
# we want this endpoint to be able to add new users and their info to this local array 
# we want to return, the full list of users 
@app.route("/userconfig", methods = ['POST'])
def add_user():
    email = request.json['email']
    gender = request.json['gender']
    country = request.json['country']
    school = request.json['school']
    if (len(users) == 0):
        user_id = 1
    else:
        user_id = users[-1]['user-id'] + 1
    newUser = {
        "user-id": user_id,
        "email": email,
        "gender": gender,
        "country": country,
        "school": school
    }
    users.append(newUser)
    return jsonify(users)

# register callback endpoint - post 
# jason
@app.route("/registercallback")
def temp():
    return "Hello World!"

# startSession endpoint - post
# jason
@app.route("/start")
def start_session():
    return temp

# endSession endpoint - post
# anthony 
# update data and turn status into False
# return that session 
@app.route("/end", methods = ['POST']) 
def end_session():
    app = request.json['app']
    user_id = request.json['user-id']
    for session in sessions:
        if user_id == session['user-id'] and app == session['app']:
            if session['status']:
                session['status'] = False
                return jsonify(session)
            else:
                return "Error: session is not active."
    return "Error: no session found."

# currentSession endpoint - get 
# anthony 
# make a temp session array/json structure where we store all the sessions 
# return the session that is currently active 
@app.route("/current", methods = ['GET'])
def get_current_session():
    for session in sessions:
        if session['status']:
            return jsonify(session)
    return "No active sessions!"

if __name__ == '__main__':
    app.run(debug=True, port=5001)