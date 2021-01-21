from flask_wtf	import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo ,Email, ValidationError
from model import UsuarioDB

class FormularioDeRegistro(FlaskForm):
	Usuario =StringField('Usuario', 
						validators = [DataRequired(),Length(min= 2, max=20)]) 

	Email = StringField('Email',
						validators=[DataRequired(), Email()])

	Senha= PasswordField('Senha',
						validators=[DataRequired(),Length(min=5,max=20)])

	ConfirmarSenha= PasswordField('Confirme Senha',
						validators=[DataRequired(),Length(min=5,max=20), EqualTo('Senha')])

	Confirma=SubmitField('Cadastre-se')

	def validate_Usuario(self, Usuario):
		user = UsuarioDB.query.filter_by(UsernameDB = Usuario.data).first()
		if user:
			raise ValidationError('Esse usuario já existe por favor inserir novo')
	def validate_Email(self, Email):
		user = UsuarioDB.query.filter_by(EmailDB = Email.data).first()
		if user:
			raise ValidationError('Esse email já existe por favor inserir novo')

class FormularioDeLogin(FlaskForm):
	Usuario =StringField('Usuario', 
						validators = [DataRequired(),Length(min= 2, max=20)]) 

	Email = StringField('Email',
						validators=[DataRequired(), Email()])
	Lembrete= BooleanField("Lembre-se de mim")

	Senha= PasswordField('Senha',
						validators=[DataRequired(),Length(min=5,max=20)])

	Entrar=SubmitField('Entre')

class AtualizarRegistro(FlaskForm):
	Usuario =StringField('Usuario', 
						validators = [DataRequired(),Length(min= 2, max=20)]) 

	Email = StringField('Email',
						validators=[DataRequired(), Email()])	

	Confirma=SubmitField('Atualizar')

	def validate_Usuario(self, Usuario):
		if Usuario.data != current_user.UsernameDB:
			user = UsuarioDB.query.filter_by(UsernameDB = Usuario.data).first()
			if user:
				raise ValidationError('Esse usuario já existe por favor inserir novo')

	def validate_Email(self, Email):
		if Email.data != current_user.EmailDB:
			user = UsuarioDB.query.filter_by(EmailDB = Email.data).first()
			if user:
				raise ValidationError('Esse email já existe por favor inserir novo')