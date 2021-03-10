import os
from flask_mail import Message
from FlaskCodePacote import mail
from FlaskCodePacote.Modelos import Dado, UsuarioDB
from sqlalchemy import desc
from datetime import datetime

def enviar_email_checkup():
	users= ['1','2']
	datahoje=datetime.utcnow
	for user  in users:
		primeiradata= Dado.query.load_only(Dado.user_id, Dado.DataDeInsercao).filter_by(user_id= user).order_by(user_id=Dado.user_id.desc()).first(Dado.DataDeInsercao)
		usuarioatrasado=  UsuarioDB.load_only(UsuarioDB.id,UsuarioDB.EmailDB).filter_by(id=user).first(UsuarioDB.EmailDB)
		if (datahoje-primeiradata).days = 14:
			msg = Message('Falta de dados',sender='ivgnoreply@gmail.com', recipients= [usuarioatrasado])
			msg.body =   f''' 
Isso e um email para vc parar de ser vagabundo
'''
    		mail.send(msg)