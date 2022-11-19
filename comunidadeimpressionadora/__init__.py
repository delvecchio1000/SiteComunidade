# CONFIGURAÇÃO DO SITE
# CONFIGURAÇÃO DO APP
# CONFIGURAÇÃO DO BANCO DE DADOS

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
#from datetime import timedelta

app = Flask(__name__)

app.config['SECRET_KEY'] = '3ac9b3a5750f8a5960cff8f039aacca3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
#app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_maneger = LoginManager(app)
login_maneger.login_view = 'login'
login_maneger.login_message_category = 'alert-info'


from comunidadeimpressionadora import routes