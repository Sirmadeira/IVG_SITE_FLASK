
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from form import FormularioDeRegistro, FormularioDeLogin, AtualizarRegistro
from flask_bcrypt import Bcrypt
from model import UsuarioDB
from flask_login import LoginManager, login_user, current_user, logout_user, login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'Login'
login_manager.login_message_category = "info"
@login_manager.user_loader
def load_user(Usuario_id):
    return UsuarioDB.query.get(int(Usuario_id))


@app.route("/", methods=['GET', 'POST'])
@app.route("/Login", methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated: 
        return redirect(url_for('HomePage'))
    form = FormularioDeLogin()
    if form.validate_on_submit():
        Usuario = UsuarioDB.query.filter_by(UsernameDB = form.Usuario.data).first()
        Email = UsuarioDB.query.filter_by(EmailDB=form.Email.data).first()
        if Usuario and Email and bcrypt.check_password_hash(Usuario.PasswordDB,form.Senha.data):
            login_user(Usuario)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect (url_for('HomePage'))
        else:
            flash('Login sem sucesso favor checar usuario e senha', 'danger')
    return render_template('Login.html', title='Login', form=form)

@app.route("/Cadastro", methods=['GET', 'POST'])
def Cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('HomePage'))
    form = FormularioDeRegistro()
    if form.validate_on_submit():
    	senha_hashed = bcrypt.generate_password_hash(form.Senha.data).decode('utf-8')
    	user= UsuarioDB(UsernameDB=form.Usuario.data, EmailDB=form.Email.data, PasswordDB= senha_hashed)
    	db.session.add(user)
    	db.session.commit()
    	flash(f'Sua conta foi criada!', 'success')
    	return redirect(url_for('Login'))
    return render_template('Cadastro.html', title='Cadastro', form=form)

@app.route("/HomePage")
def HomePage():
    return render_template("HomePage.html",title = "HomePage")

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


@app.route("/Logout")
def Logout():
    logout_user()
    return redirect(url_for('HomePage'))   

@app.route("/ContaEmpresa", methods=['GET', 'POST'])
@login_required
def ContaEmpresa(): #Consertar
    form = AtualizarRegistro()
    if form.validate_on_submit():
        current_user.UsernameDB = form.Usuario.data
        current_user.EmailDB = form.Email.data
        db.session.commit()
        flash('Sua conta foi atualizada!', 'success')
        return redirect(url_for('ContaEmpresa'))
    elif request.method == 'GET':
        form.Usuario.data = current_user.UsernameDB
        form.Email.data = current_user.EmailDB
    return render_template('ContaEmpresa.html', title= 'ContaEmpresa', form=form)

if __name__ == "__main__":
	app.run(debug=True)