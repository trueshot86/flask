from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_object('flask_site.config')
socketio = SocketIO(app)

import flask_site.views
