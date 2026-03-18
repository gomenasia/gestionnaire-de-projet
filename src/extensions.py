from flask_socketio import SocketIO

socketio = SocketIO(async_mode='gevent') # permet la connexion au canal de comunication
