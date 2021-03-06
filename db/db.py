import mysql.connector

# Herramientas
import datetime
import logging
import base64

# Config LOGS
logging.basicConfig(filename='db.log', level=logging.DEBUG)

class SQLOperations(object):
    def __init__(self):
        '''
        Configuración de DB por entorno local
        '''
        self.error = {
                'success': False,
                'message': None,
                'payload': None,
            }
        self.success = {
                'success': True,
                'message': None,
                'payload': None,
            }
        self.host = 'database-arq.cc0sxaunqcsm.sa-east-1.rds.amazonaws.com'
        self.user = 'admin'
        self.passwd = 'Arq#2022'
        self.database = 'db_arq'
        self.based = None
        self.ncursor = None
    
    #LogIn - LogOut
    def login_database(self):
        '''
        Iniciamos conexión a la db
        '''
        try:
            self.based = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.passwd,
                database=self.database
            )
            return self.based.cursor()
        except mysql.connector.Error as error:
            print('Login database Error: ' + str(error))
            self.error['message'] = str(error)
            return self.error
    
    def logout_database(self, ncursor):
        '''
        Cerrar conexión a la db
        '''
        try:
            self.ncursor = ncursor
            self.ncursor.close()
            self.based.close()
            self.based = None
        except mysql.connector.Error as error:
            print('Logout database Error: ' + str(error))
            self.error['message'] = str(error)
            return self.error
    
    # Procesos para TOKENS
    def consultar_block_tokens(self):
        '''
        Devuelve todos los block tokens
        '''
        try:
            self.ncursor = self.login_database()
            self.query = "SELECT * FROM token_blocklist"
            self.ncursor.execute(self.query)
            result = self.ncursor.fetchall()
            self.logout_database(self.ncursor)
            if result:
                return [result,True]
            return ['No hay blocktokens', False]
        except mysql.connector.Error as error: 
            print('Consultar block tokens Error: '+str(error))
            return ['Falló la consulta de block token', False]

    def consultar_token_blocklist(self, jti):
        '''
        Consulta la información específica de un token block_list
        Args:
            jti:jti 
        '''
        print('JTI db.py: ' + str(jti))
        try:
            self.ncursor = self.login_database()
            self.query = "SELECT * FROM token_blocklist WHERE n_jti = %s"
            self.ncursor.execute(self.query, (jti, ))
            result = self.ncursor.fetchone()
            print('Token block list buscado: ' + str(result))
            self.logout_database(self.ncursor)
            if result != None:
                return [result,True]
            return [None, False]
        except mysql.connector.Error as error:
            print('Consultar token blocklist Error: '+str(error))
            return ['Falló la consulta de block token', False]
    
    def clean_block_tokens(self):
        '''
        Borra los tokens vencidos de la lista de block tokens
        '''
        try:
            block_tokens = self.consultar_block_tokens()
            if block_tokens[1] == True:
                self.ncursor = self.login_database()
                self.ncursor.execute("SET SQL_SAFE_UPDATES = 0")
                for data_block_tokens in block_tokens[0]:
                    if data_block_tokens[2] < datetime.datetime.now(): #Fecha SQL < Fecha Now
                        self.query = "DELETE FROM token_blocklist WHERE k_token = %s"
                        self.ncursor.execute(self.query, (data_block_tokens[0], ))
                        self.based.commit()
                self.logout_database(self.ncursor)
            return ['Block Tokens Cleaned', True]
        except mysql.connector.Error as error:
            print('clean_block_tokens Error: '+ str(error))
            return ['Falló el proceso: Clean Block Tokens', False]
    # SELECT
    def consultar_usuario(self, id):
        '''
        Consulta la información específica de un usuario
        Args:
            id: int
        '''
        try:
            self.ncursor = self.login_database()
            self.query = "SELECT * FROM users WHERE k_users = %s"
            self.ncursor.execute(self.query, (id, ))
            result = self.ncursor.fetchone()
            self.logout_database(self.ncursor)
            if result:
                return [result,True]
            return ['Usuario no encontrado', False]
        except mysql.connector.Error as error:
            print('Consultar usuario Error: ' + str(error))
            return ['Consultar usuario Error: ', False]

    # INSERT
    def registrar_usuario(self, info):
        '''
        Registramos un usuario
        Args:
            info: Dicc
                info: sin info == Null // None
        '''
        try:
            #Verificamos que el usuario no este registrado ya
            id_user = info['id']
            self.ncursor = self.login_database()
            self.query = "SELECT * FROM users WHERE k_users = %s"
            self.ncursor.execute(self.query, (id_user,))
            user = self.ncursor.fetchone()
            self.logout_database(self.ncursor)
            if not user:
                self.ncursor = self.login_database()
                self.query = "INSERT INTO users VALUES (%s, %s, %s, %s, %s)"
                self.ncursor.execute(self.query, (info['id'], info['name'],info['correo'], info['categoria'],info['password']))
                self.based.commit()
                self.logout_database(self.ncursor)
                return ['Añadido', True]
            return [f'El usuario con ID {id_user} ya se encuentra registrado.',False]
        except mysql.connector.Error as error:
            print('Registrar usuario Error: '+str(error))
            return ['Falló el registro del usuario', False]
    
    def insertar_token_blocklist(self, jti, date):
        '''
        Registramos un token blocklist
        Args:
            jti: jti
            date: created at
        '''
        try:
            self.ncursor = self.login_database()
            self.query = "INSERT INTO token_blocklist VALUES (NULL, %s, %s)"
            self.ncursor.execute(self.query, (jti, date))
            self.based.commit()
            self.logout_database(self.ncursor)
            return ['Añadido', True]
        except mysql.connector.Error as error:
            print('Insertar token blocklist Error: '+str(error))
            return ['Falló el registro del token', False]
    
    def create_alert(self, image):
        '''
        Creamos una alerta recibiendo la imagen del hardware
        Args:
            image: 
        '''
        try:              
            self.today_date = datetime.datetime.now().strftime('%Y-%m-%d')
            self.ncursor = self.login_database()
            self.query = 'INSERT INTO alertas VALUES (NULL, %s, %s)'
            self.ncursor.execute(self.query, (self.today_date,image))
            self.based.commit()
            return ['Alerta añadida satisfactoriamente.', True]
        except mysql.connector.Error as error:
            print('Create alert Error: ' + str(error))
            return ['Falló el registro de alert', False]

    def get_alerts(self):
        '''
        Trae todas las alertas registradas en la db
        '''
        try:
            self.ncursor = self.login_database()
            self.query = "SELECT * FROM alertas ORDER BY k_alerta DESC, f_alerta DESC;"
            self.ncursor.execute(self.query)
            alerts = self.ncursor.fetchall()
            self.logout_database(self.ncursor)
            if alerts:
                return [[(data[0], data[1], base64.b64encode(data[2]).decode()) for data in alerts],True]
            return ['No hay alertas registradas', False]
        except mysql.connector.Error as error:
            print('Create alert Error: ' + str(error))
            return ['Falló la consulta de alertas', False]
    
    def set_date(self, id_dispositivo, start_date, end_date):
        '''
        Configura el intervalo de horario para el funcionamiento
        del dispositivo
        Args:
            - id_dispositivo: VARCHAR ID
            - start_date = FECHA INICIO
            - end_date = FECHA FINAL
        '''
        try:
            # Verificamos si tiene fecha asignada
            self.ncursor = self.login_database()
            self.query = "SELECT * FROM fecha_alarma WHERE k_dispositivo = %s"
            self.ncursor.execute(self.query, (id_dispositivo,))
            date_alert = self.ncursor.fetchone()
            self.logout_database(self.ncursor)
            if date_alert:
                #Si existe hacemos update
                self.ncursor = self.login_database()
                self.ncursor.execute("SET SQL_SAFE_UPDATES = 0")
                self.query = "UPDATE fecha_alarma SET f_start = %s, f_end = %s WHERE k_dispositivo = %s"
                self.ncursor.execute(self.query, (start_date, end_date, id_dispositivo,))
                self.based.commit()
                self.logout_database(self.ncursor)
                return ['Horario configurado satisfactoriamente', True]
            # Si no existe hacemos insert
            self.ncursor = self.login_database()
            self.query = "INSERT INTO fecha_alarma VALUES (NULL,%s,%s, %s)"
            self.ncursor.execute(self.query, (start_date, end_date, id_dispositivo,))
            self.based.commit()
            self.logout_database(self.ncursor)
            return ['Horario configurado satisfactoriamente', True]
        except mysql.connector.Error as error:
            print('Set alert error: ' + str(error))
            return ['Falló la configuración de alertas', False]
    
    def get_date(self, id_dispositivo):
        '''
        Devuelve el horario configurado en el dispositivo
        '''
        try:
            self.ncursor = self.login_database()
            self.query = "SELECT f_start, f_end FROM fecha_alarma WHERE k_dispositivo = %s"
            self.ncursor.execute(self.query,(id_dispositivo,))
            horario = self.ncursor.fetchone()
            self.logout_database(self.ncursor)
            if horario:
                return [horario, True]
            return ['No tiene horario configurado', False]
        except mysql.connector.Error as error:
            print('Get alert date error: ' + str(error))
            return ['Falló la consulta de horario de alertas', False]
    