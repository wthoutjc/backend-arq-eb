# Desarrollado por: https://github.com/wthoutjc
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
from mysql.connector.errors import Error

#JSON Web Tokens
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt

# Database
from db.db import SQLOperations

# Client
from client import SocketIOClient

# Herramientas
import json                     # Estructura json
import datetime                 # Manejo de fechas
from decouple import config

from decimal import Decimal
application = Flask(__name__)

app = application

app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']
db_operations = SQLOperations()

socketio_client = SocketIOClient(app)

class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return float(obj)
    return json.JSONEncoder.default(self, obj)

# JSON WEB TOKEN
jwt = JWTManager(app)

@app.route("/")
def hello_world():
    return 'Connected'

if __name__ == '__main__':
    app.run(host='0.0.0.0')