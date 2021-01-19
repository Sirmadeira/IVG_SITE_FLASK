from flask_wtf	import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo ,Email


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

	def validate_field(self, field):
		if True:
			raise ValidationError('Validation message')

class FormularioDeLogin(FlaskForm):
	Usuario =StringField('Usuario', 
						validators = [DataRequired(),Length(min= 2, max=20)]) 

	Email = StringField('Email',
						validators=[DataRequired(), Email()])
	Lembrete= BooleanField("Lembre-se de mim")

	Senha= PasswordField('Senha',
						validators=[DataRequired(),Length(min=5,max=20)])

	Entrar=SubmitField('Entre')