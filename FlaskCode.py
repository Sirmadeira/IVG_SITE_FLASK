from flask import Flask, render_template , url_for
from formularios import FormularioDeRegistro, FormularioDeLogin
app=Flask(__name__)
app.config['CHAVE_SEGREDO'] = 'e4e0a64a5879d4ce983fa8d1b24ed354' 

@app.route("/")
@app.route("/Login")
def Login():
	return render_template("Login.html")

@app.route("/Sobre")
def Sobre():
	return render_template("Sobre.html", title="Sobre")

@app.route("/SegundaJanela")
def SegundaJanela():
	return render_template("SegundaJanela.html", title = "SegundaJanela")
	
@app.route("/TerceiraJanela")
def TerceiraJanela():
	return render_template("TerceiraJanela.html", title= "TerceiraJanela")

@app.route("/HomePage")
def HomePage():
	return render_template("HomePage.html")

@app.route("/Contato")
def Contato():
	return render_template("Contato.html")

if __name__ == "__main__":
	app.run(debug=True)