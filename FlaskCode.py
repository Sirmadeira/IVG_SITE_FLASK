
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from form import FormularioDeRegistro, FormularioDeLogin
from flask_bcrypt import Bcrypt
from model import UsuarioDB

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
 
@app.route("/")
@app.route("/HomePage")
def HomePage():
	return render_template("HomePage.html",title = "HomePage")

@app.route("/Cadastro", methods=['GET', 'POST'])
def Cadastro():
    form = FormularioDeRegistro()
    if form.validate_on_submit():
    	senha_hashed = bcrypt.generate_password_hash(form.Senha.data).decode('utf-8')
    	user= UsuarioDB(UsernameDB=form.Usuario.data, EmailDB=form.Email.data, PasswordDB= senha_hashed)
    	db.session.add(user)
    	db.session.commit()
    	flash(f'Sua conta foi criada!', 'success')
    	return redirect(url_for('Login'))
    return render_template('Cadastro.html', title='Cadastro', form=form)

@app.route("/Login", methods=['GET', 'POST'])
def Login():
    form = FormularioDeLogin()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('Voce foi cadastrado', 'success')
            return redirect(url_for('HomePage'))
        else:
            flash('Login sem sucesso favor checar usuario e senha', 'danger')
    return render_template('Login.html', title='Login', form=form)



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