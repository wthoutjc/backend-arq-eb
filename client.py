#Configuración de SocketIO
from flask_socketio import SocketIO
from flask_cors import CORS

# # Hilos
from threading import Thread, Event

# # Herramientas
import logging
import json

import eventlet

# # Globals
socketio = None
# # thread = Thread()
# # thread_stop_event = Event()

# # Config LOGS
logging.basicConfig(filename='client.log', level=logging.DEBUG)

class SocketIOClient(object):
    def __init__(self, app):
        global socketio
        self.app = app
        CORS(self.app)
        socketio = SocketIO(app, cors_allowed_origins='*',async_mode="eventlet") #cors_allowed_origins="*", async_mode="eventlet" http://frontend-arq.s3-website-sa-east-1.amazonaws.com/
        self.connected_clients = {}
    
    def run(self):
        # Posible inclusión de Threads

        # Rutas
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
            socketio.emit('message', {'message': 'Enviado desde backend'})

        # Conexión
        socketio.run(self.app, host="0.0.0.0", port=80, debug=True) #host="0.0.0.0"
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