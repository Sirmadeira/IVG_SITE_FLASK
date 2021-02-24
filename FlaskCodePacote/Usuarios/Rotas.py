from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from FlaskCodePacote import db, bcrypt
from FlaskCodePacote.Modelos import UsuarioDB
from FlaskCodePacote.Usuarios.Formularios import (FormularioDeRegistro,FormularioDeLogin, AtualizarRegistro,RequisitarReset,
                                        ResetSenhaForm)
from FlaskCodePacote.Usuarios.Utilidades import enviar_email_reset


Usuarios= Blueprint('Usuarios', __name__)




@Usuarios.route("/Cadastro", methods=['GET', 'POST'])
def Cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('Principal.HomePage'))
    form = FormularioDeRegistro()
    if form.validate_on_submit():
        senha_hashed = bcrypt.generate_password_hash(form.Senha.data).decode('utf-8')
        user= UsuarioDB(UsernameDB=form.Usuario.data,NomeDaEmpresaDB= form.NomeDaEmpresa.data,ComercioDB= form.Comercio.data,
                        EmailDB=form.Email.data, PasswordDB= senha_hashed)
        db.session.add(user)
        db.session.commit()
        flash(f'Sua conta foi criada!', 'success')
        return redirect(url_for('Usuarios.Login'))
    return render_template('Cadastro.html', title='Cadastro', form=form)

@Usuarios.route("/Login", methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('Principal.HomePage'))
    form = FormularioDeLogin()
    if form.validate_on_submit():
        UsuarioLogado = UsuarioDB.query.filter_by(UsernameDB = form.Usuario.data).first()
        Email = UsuarioDB.query.filter_by(EmailDB=form.Email.data).first()
        if UsuarioLogado and Email and bcrypt.check_password_hash(UsuarioLogado.PasswordDB,form.Senha.data):
            login_user(UsuarioLogado,remember=form.Lembrete.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect (url_for('Principal.HomePage'))
        else:
            flash('Login sem sucesso favor checar usuario e senha', 'danger')
    return render_template('Login.html', title='Login', form=form)

@Usuarios.route("/Logout")
def Logout():
    logout_user()
    return redirect(url_for('HomePage'))   

@Usuarios.route("/ContaEmpresa", methods=['GET', 'POST'])
@login_required
def ContaEmpresa():
    form = AtualizarRegistro()
    if form.validate_on_submit():
        current_user.UsernameDB = form.Usuario.data
        current_user.EmailDB = form.Email.data
        db.session.commit()
        flash('Sua conta foi atualizada!', 'success')
        return redirect(url_for('Usuarios.ContaEmpresa'))
    elif request.method == 'GET':
        form.Usuario.data = current_user.UsernameDB
        form.Email.data = current_user.EmailDB
    return render_template('ContaEmpresa.html', title= 'ContaEmpresa', form=form)

@Usuarios.route("/ResetSenha", methods=['GET', 'POST'])
def ResetSenha():
    if current_user.is_authenticated:
        return redirect(url_for('Principal.HomePage'))
    form = RequisitarReset()
    if form.validate_on_submit():
        user=UsuarioDB.query.filter_by(EmailDB= form.Email.data).first()  
        enviar_email_reset(user)
        flash(' Um email foi enviado com instruções.', 'info')  
        return redirect(url_for('Usuarios.Login'))
    return render_template('ResetPedido.html', title = 'Resetar senha',form = form)


@Usuarios.route("/ResetSenha/<token>", methods=['GET', 'POST'])
def Reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('Principal.HomePage'))
    user=UsuarioDB.verify_reset_token(token)
    if user is None:
        flash(' Esse token não é mais valído', ' warning')
        return redirect(url_for('Usuarios.ResetSenha'))
    form = ResetSenhaForm()
    if form.validate_on_submit():
        senha_hashed = bcrypt.generate_password_hash(form.Senha.data).decode('utf-8')
        user.PasswordDB = senha_hashed
        db.session.commit()
        flash(f'Sua senha foi resetada!', 'success')
        return redirect(url_for('Usuarios.Login'))
    return render_template('ResetToken.html', title = 'Resetar senha',form = form)