import mysql.connector

# Herramientas
import datetime
import logging

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
            self.query = 'INSERT INTO alertas VALUES (NULL, %s, %s)'
            self.image = image.read()
            self.ncursor.execute(self.query, (self.today_date,self.image))
            self.based.commit()
            return ['Alerta añadida satisfactoriamente.', True]
        except mysql.connector.Error as error:
            print('Create alert Error: ' + str(error))
            return ['Falló el registro de alert', False]
