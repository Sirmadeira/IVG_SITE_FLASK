from flask import Flask, render_template , url_for
from form import FormularioDeRegistro, FormularioDeLogin


app=Flask(__name__)
app.config['SECRET_KEY'] = 'a3c293dd89c6703bfa4836e4059e3cdf'
@app.route("/")
@app.route("/HomePage")
def HomePage():
	return render_template("HomePage.html",title = "HomePage")

@app.route("/Cadastro")
def Cadastro():
	form = FormularioDeRegistro()
	return render_template('Cadastro.html',title = "Cadastro", form = form)

@app.route("/Login")
def Login():
	form= FormularioDeLogin()
	return render_template("Login.html",title= "Login", form = form)

@app.route("/Sobre")
def Sobre():
	return render_template("Sobre.html", title = "Sobre")

@app.route("/SegundaJanela")
def SegundaJanela():
	return render_template("SegundaJanela.html", title = "SegundaJanela")
	
@app.route("/TerceiraJanela")
def TerceiraJanela():
	return render_template("TerceiraJanela.html", title = "TerceiraJanela")

@app.route("/Contato")
def Contato():
	return render_template("Contato.html", title = "Contato")

if __name__ == "__main__":
	app.run(debug=True)