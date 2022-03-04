#Configuración de SocketIO
from flask_socketio import SocketIO
from flask_cors import CORS
from flask import jsonify

# # Hilos
from threading import Thread, Event
import threading

# # Herramientas
import logging
import json
import datetime
import eventlet
import base64

from random import seed
from random import random

seed(datetime.datetime.now())

# # Globals
# # thread = Thread()
# # thread_stop_event = Event()

# # Config LOGS
logging.basicConfig(filename='client.log', level=logging.DEBUG)

class SocketIOClient(object):
    def __init__(self, app):
        self.app = app
        CORS(self.app)
        self.socketio = SocketIO(app, cors_allowed_origins='*',async_mode="threading") #cors_allowed_origins="*", async_mode="eventlet" http://frontend-arq.s3-website-sa-east-1.amazonaws.com/
        self.connected_clients = {}
    
        @self.socketio.on('connect')
        def on_connect():
            # global thread
            print(f'Cliente ff conectado satisfactoriamente')

            # if not thread.is_alive():
            #     thread = RandomThread()
            #     thread.start()

        @self.socketio.on('disconnect')
        def on_disconnect():
            print(f'Cliente ff desconectado satisfactoriamente.')

        @self.socketio.on('messages')
        def on_messages(*args):
            # response = [json.loads(data) for data in args]
            # print(response)
            random_number = int(random() * 1000)
            print(random_number)
            self.socketio.emit('message', {'message': random_number})

    def emit_alert(self, file):
        '''
        Emite una alerta
        '''
        # results['image'] = base64.b64encode(file).decode()
        # print(results['image'])
        self.socketio.emit('alert', {'image': file})

    def run(self):
        self.socketio.run(self.app, port=8000, host="0.0.0.0", debug=True) #host="0.0.0.0" port=80
        eventlet.monkey_patch(socket=True, select=True)

class RandomThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RandomThread, self).__init__()

    def random_number_generator(self):
        print(f'Generando aleatorios')

        # while not thread_stop_event.is_set():
        #     number = round(random() * 10, 3)
        #     socketio.emit('new_number',  {'number': number}) # Pendiente por multi hilo (DE REQUERIRSE)
        #     thread_stop_event.set()
        #     sleep(self.delay)

        print(f'End')

    def start(self):
        self.random_number_generator()