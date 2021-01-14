from flask_wtf	import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo	

class FormularioDeRegistro(FlaskForm):
	Usuario =StringField('Usuario', 
						validators = [DataRequired(),Length(min= 2, max=20)]) 

	Email = StringField('Email',
						validators=[DataRequired(),Email()])

	Senha= PasswordField('Senha',
						validators=[DataRequired(),Length(min=5,max=20)])

	ConfirmaSenha= PasswordField('ConfirmaSenha',
						validators=[DataRequired(),Length(min=5,max=20), EqualTo('Senha')])

	Confirma=SubmitField('Cadastre-se')

class FormularioDeLogin(FlaskForm):
	Usuario =StringField('Usuario', 
						validators = [DataRequired(),Length(min= 2, max=20)]) 

	Email = StringField('Email',
						validators=[DataRequired(),Email()])

	Lembrete= BooleanField("Lembre-se de mim")

	Senha= PasswordField('Senha',
						validators=[DataRequired(),Length(min=5,max=20)])
	Confirma=SubmitField('Entre')