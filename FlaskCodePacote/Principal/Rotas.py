from flask import render_template, request, Blueprint

Principal = Blueprint('Principal', __name__)


@Principal.route("/", methods=['GET', 'POST'])
@Principal.route("/HomePage", methods=['GET', 'POST'])
def HomePage():
    return render_template("HomePage.html",title = "HomePage")


@Principal.route("/Sobre")
def Sobre():
    return render_template("Sobre.html", title = "Sobre")
