from flask import Flask, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room, rooms
from os import environ

app = Flask(__name__)

socketio = SocketIO(app,logger=False,engineio_logger=False,cors_allowed_origins = '*')

socket_rooms = []

@app.route("/")
def home():
    return "Welcome to Blackbeard's Island Socket API"

@socketio.on('connect')
def connection():
    print('A new player just connected -- ' + request.sid)

@socketio.on('disconnect')
def disconnect():
    socket_to_delete = None
    for i in range(len(socket_rooms)):
        if socket_rooms[i]['socket'] == str(request.sid):
            socket_to_delete = i
            if socket_rooms[i]['isHost'] == False:
                emit('player disconnected', str(request.sid), to = socket_rooms[i]['room'])
            else:
                player_index = next((j for j, item in enumerate(socket_rooms) if item['room'] == socket_rooms[i]['room'] and item['isHost'] != True), None)
                if player_index != None:
                    socket_rooms[player_index]['isHost'] = True
                    emit('host disconnected', to = socket_rooms[player_index]['socket'])
                    
    if socket_to_delete != None:
        del socket_rooms[socket_to_delete]

@socketio.on('create game')
def createRoom(gameData):
    roomID = gameData["roomID"]

    join_room(roomID)
    socket_rooms.append({'socket':str(request.sid),'room':roomID, 'isHost':True})

    print("Room ID "+ roomID + " has been created")
    emit('change state', gameData, to = roomID)

@socketio.on('join game')
def joinRoom(joiningData):
    roomID = joiningData["roomID"]
    username = joiningData["player"]["user"]
    userSocket = joiningData["player"]["id"]

    socket_rooms.append({'socket':str(request.sid),'room':roomID, 'isHost':False})
    join_room(roomID)

    print('Player ' + username + " just joined Room "+ roomID)
    emit('user joining waiting room', joiningData, to = roomID, include_self=False)

@socketio.on('send state to players')
def lobby(gameData):
    roomID = gameData["roomID"]
    emit('change state', gameData, to = roomID)

@socketio.on('move')
def lobby(position):
    print(position["x"])
#     roomID = gameData["roomID"]
#     emit('change state', gameData, to = roomID)


if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))
    socketio.run(app, debug=False, port=port)