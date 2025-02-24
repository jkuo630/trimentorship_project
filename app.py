from flask import Flask, jsonify, request
from flask_cors import CORS


# Create Flask's `app` object
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def hello():
    return "Hello World!"


leaderboard = [
    {
        "pfp": "/pfps/jason.jpg",
        "username": "jkuo630",
        "score": 1200,
        "location": "UBC",
        "postTime": "2hr ago",
        "postMedia": "/jason.mp4",
    },
    {
        "pfp": "/pfps/jay.png",
        "username": "therealjaypark",
        "score": 980,
        "location": "SFU",
        "postTime": "3hr ago",
        "postMedia": "/jay.mp4",
    },
]

@app.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    """Fetch the current leaderboard."""
    print("DOING THIS")
    response = jsonify(leaderboard)
    response.headers["Content-Type"] = "application/json"
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5001)