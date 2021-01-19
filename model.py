from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
 

class UsuarioDB(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	UsernameDB = db.Column(db.String(20), unique=True, nullable=False)
	EmailDB = db.Column(db.String(120), unique=True, nullable=False)	
	PasswordDB = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return f"User('{self.UsernameDB}', '{self.EmailDB}')"