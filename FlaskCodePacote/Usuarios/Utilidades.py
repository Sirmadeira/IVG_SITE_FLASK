import os
from flask import url_for
from flask_mail import Message
from FlaskCodePacote import mail



def enviar_email_reset(user):
    token = user.get_reset_token()
    msg = Message('Reset de Email',sender='ivgnoreply@gmail.com', recipients= [user.EmailDB])
    msg.body =   f''' 

Para resetar sua senha, visite o link a seguir:
Se você não fez esse pedido então simplesmente ignore esse E-mail. 
Caso você o tenha feito então só clicar no link abaixo


{url_for('Usuarios.Reset_token', token= token, _external= True)}


Caso você tenha problemas favor nos contatar pelos contatos expostos no site.
'''
    mail.send(msg)