import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request
from flask_socketio import SocketIO
from typing import Callable

def server(on_user_message: Callable[[str, SocketIO], None]):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app, cors_allowed_origins="*")

    @app.route('/')
    def index():
        return render_template('index.html')

    @socketio.on('connect')
    def on_connect():
        print(f"[+] {request.remote_addr} connected")

    @socketio.on('disconnect')
    def on_disconnect():
        print(f"[-] {request.remote_addr} disconnected")

    @socketio.on('message')
    def handle_message(msg):
        print(f"User says: {msg}")
        on_user_message(msg, socketio)

    return app, socketio