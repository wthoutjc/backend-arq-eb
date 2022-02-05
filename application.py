# Desarrollado por: https://github.com/wthoutjc
from flask import Flask

application = Flask(__name__)

@application.route("/")
def hello_world():
    return 'Connected'

if __name__ == '__main__':
    application.run()
