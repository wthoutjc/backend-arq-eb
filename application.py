# Desarrollado por: https://github.com/wthoutjc
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
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
import os

from decimal import Decimal

from flask_socketio import SocketIO
from flask_cors import CORS

import eventlet

application = Flask(__name__)

app = application

CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*',async_mode="threading") #cors_allowed_origins="*", async_mode="eventlet" http://frontend-arq.s3-website-sa-east-1.amazonaws.com/

from random import seed
from random import random

seed(datetime.datetime.now())

@app.route("/")
def hello_world():
    return make_response(jsonify({"res": 'Connected'}), 200)

@socketio.on('connect')
def on_connect():
    # global thread
    print(f'Cliente conectado satisfactoriamente')

    # if not thread.is_alive():
    #     thread = RandomThread()
    #     thread.start()

@socketio.on('disconnect')
def on_disconnect():
    print(f'Cliente desconectado satisfactoriamente.')

@socketio.on('messages')
def on_messages(*args):
    response = [json.loads(data) for data in args]
    print(response)
    socketio.emit('message', {'message': int(random() * 1000)})

# Conexión
if __name__ == '__main__':
    socketio.run(app, port=8000, host="0.0.0.0", debug=True) #host="0.0.0.0" port=80
    eventlet.monkey_patch(socket=True, select=True)

# app.config['SECRET_KEY'] = 'UHGx14#&17NoPRQS#12'
# app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']
# db_operations = SQLOperations()

# socketio_client = SocketIOClient(app)

# class DecimalEncoder(json.JSONEncoder):
#   def default(self, obj):
#     if isinstance(obj, Decimal):
#       return float(obj)
#     return json.JSONEncoder.default(self, obj)

# # JSON WEB TOKEN
# jwt = JWTManager(app)

# @jwt.token_in_blocklist_loader
# def check_if_token_revoked(jwt_header, jwt_payload):
#     jti = jwt_payload["jti"]
#     try:
#         print('Consultando token block list')
#         token, success = db_operations.consultar_token_blocklist(jti)
#         if success == True:
#             return token is not None
#     except Error as error:
#         print('Check token revoked Error: ' + str(error))
#         return False

# @app.route("/")
# def hello_world():
#     return make_response(jsonify({"res": 'Connected'}), 200)

# # Rutas SQL
# @app.route("/log-in", methods=["POST"])
# def log_in():
#     print('log-in')
#     message, success = db_operations.clean_block_tokens()
#     if request.data and success:
#         data_raw = request.data.decode("utf-8")
#         json_data = json.loads(data_raw)

#         username = json_data['username']
#         password = json_data['password']

#         if username:
#             if password:  
#                 logIn = db_operations.consultar_usuario(username)
#                 print('LogIn: ' + str(logIn[1]))
#                 if logIn[1] == True and check_password_hash(logIn[0][4], password):
#                     payload = {
#                         'id': logIn[0][0],
#                         'name': logIn[0][1],
#                         'correo': logIn[0][2],
#                         'categoria': logIn[0][3]
#                     }
#                     access_token = create_access_token(identity=payload, expires_delta=datetime.timedelta(hours=7))
#                     return make_response(jsonify({"results": access_token}), 200)
#                 return make_response(jsonify({"results": 'Usuario o contraseña incorrectas'}), 500)
#             return make_response(jsonify({"results": 'Contraseña no ingresada'}), 500)
#         return make_response(jsonify({"results": 'Usuario no ingresado'}), 500)
#     return make_response(jsonify({"results": 'Falló el procesamiento de la solicitud.'}), 500)

# # Registar por ruta abierta
# @app.route("/register-nojwt", methods=["POST"])
# def register_no_jwt():
#     print('register_no_jwt')
#     if request.method == "POST":

#         data_raw = request.data.decode("utf-8")
#         json_data = json.loads(data_raw)

#         if json_data['id'] == None:
#             return make_response(jsonify({"results": 'La ID es un campo obligatorio'}), 500)
#         if json_data['name'] == None:
#             return make_response(jsonify({"results": 'Nombre es un campo obligatorio'}), 500)
#         if json_data['correo'] == None:
#             return make_response(jsonify({"results": 'Correo es un campo obligatorio'}), 500)
#         if json_data['password'] == None:
#             return make_response(jsonify({"results": 'Contraseña es un campo obligatorio'}), 500)
#         json_data_with_hash = {
#             "id": json_data['id'],
#             "name": json_data['name'],
#             "correo": json_data['correo'],
#             "categoria": json_data['categoria'],
#             "password": generate_password_hash(json_data['password']),
#         }
#         message, success = db_operations.registrar_usuario(json_data_with_hash)
#         if success:
#             return make_response(jsonify({"results": 'Usuario registrado satisfactoriamente'}), 200)
#         else:
#             return make_response(jsonify({"results": message}), 500)
#     return make_response(jsonify({"results": 'Falló la comunicación con el servidor'}), 500)

# @app.route("/revokeToken", methods=["DELETE"])
# @jwt_required()
# def modify_token():
#     print('modify_token')
#     jti = get_jwt()["jti"]
#     print('revokeToken JTI: ' + str(jti))
#     try:
#         message, success = db_operations.insertar_token_blocklist(jti, datetime.datetime.now(datetime.timezone.utc))
#         if success:
#             return make_response(jsonify({"results": "JWT revoked"}), 200)
#         return make_response(jsonify({"results": message}), 500)
#     except Error as error:
#         print('Revoke Token Error:' + str(error))
#         return make_response(jsonify({"results": 'SQL Operation Failed'}), 500)

# if __name__ == '__main__':
#     socketio_client.run()

# if __name__ == '__main__':
#     app.run(host='0.0.0.0')