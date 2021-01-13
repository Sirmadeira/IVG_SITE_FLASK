from flask import Flask, render_template
app=Flask(__name__)


@app.route("/")
@app.route("/home")
def login():
	return render_template("Login.html")

@app.route("/sobre")
def sobre():
	return render_template("Sobre.html", title="Sobre")

@app.route("/SegundaJanela")
def SegundaJanela():
	return render_template("SegundaJanela.html", title = "SegundaJanela")
	
@app.route("/TerceiraJanela")
def TerceiraJanela():
	return render_template("TerceiraJanela.html", title= "TerceiraJanela")


if __name__ == "__main__":
	app.run(debug=True)s