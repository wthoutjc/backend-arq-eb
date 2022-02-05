# Desarrollado por: https://github.com/wthoutjc
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
# from mysql.connector.errors import Error

# #JSON Web Tokens
# from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt

# Database
# from db.db import SQLOperations

# Client
# from client import SocketIOClient

# Herramientas
# import json                     # Estructura json
# import datetime                 # Manejo de fechas
# from decouple import config

# from decimal import Decimal

application = Flask(__name__)

application.config['MYSQL_HOST'] = 'database-arq.cc0sxaunqcsm.sa-east-1.rds.amazonaws.com'
application.config['MYSQL_USER'] = 'admin'
application.config['MYSQL_PASSWORD'] = 'Arq#2022'
application.config['MYSQL_DB'] = 'db_arq'
application.config['SECRET_KEY'] = 'UHGx14#&17NoPRQS#12'
# application.config['JWT_SECRET_KEY'] = 'UHGx14#&17NoPRQS#12'


mysql = MySQL(application)

@application.route("/")
def hello_world():
    return 'Connected'

if __name__ == '__main__':
    application.run(host='0.0.0.0')