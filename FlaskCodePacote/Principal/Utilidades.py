from flask_mail import Message
from FlaskCodePacote import mail, db
from FlaskCodePacote.Modelos import Dado, UsuarioDB
from sqlalchemy import desc
from datetime import datetime

def enviar_email_checkup():
	users= [1,2]
	for user in users:
		ultimadata=db.session.query(Dado.DataDeInsercao).filter_by(user_id = user).order_by(Dado.DataDeInsercao.desc()).limit(1).scalar()
		dueduser=db.session.query(UsuarioDB.EmailDB,UsuarioDB.id).filter_by(id = user).order_by(UsuarioDB.id.desc()).limit(1).scalar()
		datahoje=datetime.datetime.utcnow()
		diff= datahoje-ultimadata
		if diff.days >= 2:
			msg = Message('Falta de dados',sender='ivgnoreply@gmail.com', recipients= [dueduser])
			msg.body =   'Isso e um email para vc parar de ser vagabundo'
			mail.send(msg)
		else:
			break
