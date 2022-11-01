from flask import Flask
from flask_socketio import SocketIO, send, emit, join_room, leave_room, rooms
from os import environ

app = Flask(__name__)

socketio = SocketIO(app,logger=True,engineio_logger=True,cors_allowed_origins = '*')

@app.route("/")
def home():
    return "Welcome to Blackbeard's Island Socket API"

@socketio.on('connect')
def connection():
    print('A new player just connected')

@socketio.on('create game')
def createRoom(gameData):
    roomID = gameData["roomID"]
    join_room(roomID)
    print("Room ID "+ roomID + " has been created")
    emit('change state', gameData, to = roomID)

@socketio.on('join game')
def joinRoom(joiningData):
    roomID = joiningData["roomID"]
    username = joiningData["player"]["user"]
    userSocket = joiningData["player"]["id"]
    join_room(roomID)
    print('Player ' + username + " just joined Room "+ roomID)
    emit('user joining waiting room', joiningData, to = roomID, include_self=False)

@socketio.on('send state to players')
def lobby(gameData):
    roomID = gameData["roomID"]
    emit('change state', gameData, to = roomID)


if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))
    socketio.run(app, debug=False, port=port)