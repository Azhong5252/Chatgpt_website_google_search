from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
import eventlet

def server():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app)

    @app.route('/')
    def index():
        return render_template('index.html') 

    @socketio.on('connect')
    def on_connect():
        print(f"Client connected: {request.remote_addr}")

    @socketio.on('disconnect')
    def on_disconnect():
        print(f"Client disconnected: {request.remote_addr}")

    @socketio.on('message')
    def handle_message(msg):
        print(f"Received message: {msg}")  
        send(msg, broadcast=True)

    if __name__ == '__main__':
        socketio.run(app, host='0.0.0.0', port=80)  
if __name__ == "__main__":
    server()