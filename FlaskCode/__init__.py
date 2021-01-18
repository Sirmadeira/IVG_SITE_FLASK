from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app=Flask(__name__)
app.config['SECRET_KEY'] = 'a3c293dd89c6703bfa4836e4059e3cdf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///UsuarioIVG.db'
db= SQLAlchemy(app)
bcrypt = Bcrypt(app)


from FlaskCode import Rotas