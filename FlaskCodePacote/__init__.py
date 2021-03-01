from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from FlaskCodePacote.Config import Config

 
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'Usuarios.Login'
login_manager.login_message_category = "info"
mail= Mail()

def criar_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from FlaskCodePacote.Usuarios.Rotas import Usuarios
    from FlaskCodePacote.Tabelas.Rotas import Tabelas
    from FlaskCodePacote.Principal.Rotas import Principal
    app.register_blueprint(Usuarios)
    app.register_blueprint(Tabelas)
    app.register_blueprint(Principal)

    return app