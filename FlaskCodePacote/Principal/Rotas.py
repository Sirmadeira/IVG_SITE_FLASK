from flask import render_template, request, Blueprint
from FlaskCodePacote.Principal.Utilidades import enviar_email_checkup

Principal = Blueprint('Principal', __name__)


@Principal.route("/", methods=['GET', 'POST'])

@Principal.route("/HomePage", methods=['GET', 'POST'])
def HomePage():
	enviar_email_checkup()
	return render_template("HomePage.html",title = "HomePage")

@Principal.route("/Sobre")
def Sobre():
    return render_template("Sobre.html", title = "Sobre")

@Principal.route("/Faq")
def Faq():
    return render_template("Faq.html", title = "Faq")