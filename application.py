# Desarrollado por: https://github.com/wthoutjc
# Universidad Distrital Francisco José de Caldas
import re
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

application = Flask(__name__)

app = application

app.config['SECRET_KEY'] = 'UHGx14#&17NoPRQS#12'
app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']

db_operations = SQLOperations()
socketio = SocketIOClient(app)

class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return float(obj)
    return json.JSONEncoder.default(self, obj)

# JSON WEB TOKEN
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    try:
        print('Consultando token block list')
        token, success = db_operations.consultar_token_blocklist(jti)
        if success == True:
            return token is not None
    except Error as error:
        print('Check token revoked Error: ' + str(error))
        return False

@app.route("/")
def hello_world():
    return make_response(jsonify({"res": 'Connected'}), 200)

# Rutas SQL
@app.route("/log-in", methods=["POST"])
def log_in():
    print('log-in')
    message, success = db_operations.clean_block_tokens()
    if request.data and success:
        data_raw = request.data.decode("utf-8")
        json_data = json.loads(data_raw)

        username = json_data['username']
        password = json_data['password']

        if username:
            if password:  
                logIn = db_operations.consultar_usuario(username)
                print('LogIn: ' + str(logIn[1]))
                if logIn[1] == True and check_password_hash(logIn[0][4], password):
                    payload = {
                        'id': logIn[0][0],
                        'name': logIn[0][1],
                        'correo': logIn[0][2],
                        'categoria': logIn[0][3]
                    }
                    access_token = create_access_token(identity=payload, expires_delta=datetime.timedelta(hours=7))
                    return make_response(jsonify({"results": access_token}), 200)
                return make_response(jsonify({"results": 'Usuario o contraseña incorrectas'}), 500)
            return make_response(jsonify({"results": 'Contraseña no ingresada'}), 500)
        return make_response(jsonify({"results": 'Usuario no ingresado'}), 500)
    return make_response(jsonify({"results": 'Falló el procesamiento de la solicitud.'}), 500)

# Registar por ruta abierta
@app.route("/register-nojwt", methods=["POST"])
def register_no_jwt():
    print('register_no_jwt')
    if request.method == "POST":

        data_raw = request.data.decode("utf-8")
        json_data = json.loads(data_raw)

        if json_data['id'] == None:
            return make_response(jsonify({"results": 'La ID es un campo obligatorio'}), 500)
        if json_data['name'] == None:
            return make_response(jsonify({"results": 'Nombre es un campo obligatorio'}), 500)
        if json_data['correo'] == None:
            return make_response(jsonify({"results": 'Correo es un campo obligatorio'}), 500)
        if json_data['password'] == None:
            return make_response(jsonify({"results": 'Contraseña es un campo obligatorio'}), 500)
        json_data_with_hash = {
            "id": json_data['id'],
            "name": json_data['name'],
            "correo": json_data['correo'],
            "categoria": json_data['categoria'],
            "password": generate_password_hash(json_data['password']),
        }
        message, success = db_operations.registrar_usuario(json_data_with_hash)
        if success:
            return make_response(jsonify({"results": 'Usuario registrado satisfactoriamente'}), 200)
        else:
            return make_response(jsonify({"results": message}), 500)
    return make_response(jsonify({"results": 'Falló la comunicación con el servidor'}), 500)

@app.route("/revokeToken", methods=["DELETE"])
@jwt_required()
def modify_token():
    print('modify_token')
    jti = get_jwt()["jti"]
    print('revokeToken JTI: ' + str(jti))
    try:
        message, success = db_operations.insertar_token_blocklist(jti, datetime.datetime.now(datetime.timezone.utc))
        if success:
            return make_response(jsonify({"results": "JWT revoked"}), 200)
        return make_response(jsonify({"results": message}), 500)
    except Error as error:
        print('Revoke Token Error:' + str(error))
        return make_response(jsonify({"results": 'SQL Operation Failed'}), 500)

# Alerta
@app.route("/alert", methods=["POST"])
@jwt_required()
def create():
    print('alert')
    if request.method == "POST":
        if request.files: #En request.files van las imagenes
            image = request.files['file']
            image_process = image.read()
            message, success = db_operations.create_alert(image_process)
            if success:
                socketio.emit_alert(image_process)
                return make_response(jsonify({"results": message}), 200)
            return make_response(jsonify({"results": message}), 500)
        return make_response(jsonify({"results": 'Falló el procesamiento de la imagen.'}), 500)
    return make_response(jsonify({"results": 'Falló la comunicacíon con el servidor.'}), 500)

@app.route("/getalerts")
@jwt_required()
def get_alerts():
    print('get_alerts')
    alerts, success = db_operations.get_alerts()
    if success:
        return make_response(jsonify({"results":alerts}), 200)
    return make_response(jsonify({"results": alerts}), 500)

@app.route("/setdate", methods=["POST"])
@jwt_required()
def set_date():
    print('set_date')

    data_raw = request.data.decode("utf-8")
    json_data = json.loads(data_raw)

    id_dispositivo = json_data['idDispositivo']
    start_date = json_data['startDate']
    end_date = json_data['endDate']

    alerts, success = db_operations.set_date(id_dispositivo, start_date, end_date)
    if success:
        return make_response(jsonify({"results":alerts}), 200)
    return make_response(jsonify({"results": alerts}), 500)

@app.route("/getdate/<id>")
@jwt_required()
def get_date(id):
    print('get_date')

    alerts, success = db_operations.get_date(id)
    if success:
        return make_response(jsonify({"results":alerts}), 200)
    return make_response(jsonify({"results": alerts}), 500)

# Conexión
if __name__ == '__main__':
    socketio.run()

# socketio_client = SocketIOClient(app)

# if __name__ == '__main__':
#     socketio_client.run()

# if __name__ == '__main__':
#     app.run(host='0.0.0.0')