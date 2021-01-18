from flask import Flask, render_template , url_for, flash, redirect
<<<<<<< HEAD:FlaskCode/Rotas.py
from FlaskCode import app, db ,bcrypt 
from FlaskCode.form  import FormularioDeRegistro, FormularioDeLogin
from FlaskCode.Modelos import UsuariosDB	
=======
from flask_sqlalchemy import SQLAlchemy
from form import FormularioDeRegistro, FormularioDeLogin
>>>>>>> parent of f0c3832... Remodelando para ser um pacote ao inves de modulo:FlaskCode.py



app=Flask(__name__)
app.config['SECRET_KEY'] = 'a3c293dd89c6703bfa4836e4059e3cdf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///UsuarioIVG.db'
db= SQLAlchemy(app)

class UsuariosDB(db.Model):
	id = db.Column(db.Integer, primary_key= True)
	UsuarioDB = db.Column(db.String(20), unique= True, nullable = False)
	EmailDB = db.Column(db.String(120), unique= True, nullable = False)
	SenhaDB = db.Column(db.String(60), nullable = False)


	def __repr__(self):
		return f"UsuariosDB('{self.UsuarioDB}','{self.EmailDB}')"

		
@app.route("/")
@app.route("/HomePage")
def HomePage():
	return render_template("HomePage.html",title = "HomePage")

@app.route("/Cadastro",methods = ['GET','POST'])
def Cadastro():
	form = FormularioDeRegistro()
	if form.validate_on_submit():
		hashed_senha= bcrypt.generate_password_hash(form.Senha.data).decode('utf-8')
		UsuarioHS= UsuariosDB(UsuarioDB= form.Usuario.data, EmailDB=form.Email.data, SenhaDB= hashed_senha)
		db.session.add(UsuarioHS)
		db.session.commit()
		flash(f"Sua conta foi criado com sucesso!", 'success')
		return redirect(url_for('Login'))
	return render_template('Cadastro.html',title = "Cadastro", form = form)

@app.route("/Login", methods = ['GET', 'POST'])
def Login():
	form= FormularioDeLogin()
	if form.validate_on_submit():
		if form.Email.data == 'adming@blog.com' and form.Senha.data == 'Senha' and form.Usuario.data == 'Sirmadeira':
			flash(' Você foi cadastrado!', 'success')
			return redirect(url_for('HomePage'))
		else:
			flash(' Login sem sucesso. Por favor cheque seu usuario e senha', 'danger')
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