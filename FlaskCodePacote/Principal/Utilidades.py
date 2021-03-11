from flask_mail import Message
from FlaskCodePacote import mail, db
from FlaskCodePacote.Modelos import Dado, UsuarioDB
from sqlalchemy import desc, func
from datetime import datetime

def enviar_email_checkup():
	users= ['1','2']
	for user in users:
		lastsentdate= db.session.query(func.date(Dado.DataDeInsercao,UsuarioDB.EmailDB.label('dueduser'))).filter_by(user_id= user).order_by(Dado.id.desc()).first()
		diff = datetime.utcnow() - lastsentdate
		if diff >= 14:
			msg = Message('Falta de dados',sender='ivgnoreply@gmail.com', recipients= [dueduser])
			msg.body =   'Isso e um email para vc parar de ser vagabundo'
			mail.send(msg)
