from flask import Flask
from flask_socketio import SocketIO, send, emit
from os import environ

app = Flask(__name__)

socketio = SocketIO(app,logger=True,engineio_logger=True,cors_allowed_origins = '*')

@app.route("/")
def home():
    return "Welcome to Blackbeard's Island Socket API"

@socketio.on('connect')
def connection():
    print('A new player just connected')

if __name__ == "__main__":
    port = int(environ.get("PORT", 5001))
    socketio.run(app, debug=False, port=port)