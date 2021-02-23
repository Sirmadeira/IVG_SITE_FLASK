import secrets
from flask import render_template, url_for, flash, redirect, request
from FlaskCodePacote import app, db, bcrypt, mail
from FlaskCodePacote.Formularios import (FormularioDeRegistro,FormularioDeLogin, AtualizarRegistro,RequisitarReset,
                                        ResetSenhaForm,DadosEssenciais)
from FlaskCodePacote.Modelos import UsuarioDB, Dado
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message



@app.route("/", methods=['GET', 'POST'])
@app.route("/Login", methods=['GET', 'POST'])
def Login():
    form = FormularioDeLogin()
    if form.validate_on_submit():
        Usuario = UsuarioDB.query.filter_by(UsernameDB = form.Usuario.data).first()
        Email = UsuarioDB.query.filter_by(EmailDB=form.Email.data).first()
        if Usuario and Email and bcrypt.check_password_hash(Usuario.PasswordDB,form.Senha.data):
            login_user(Usuario,remember=form.Lembrete.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect (url_for('HomePage'))
        else:
            flash('Login sem sucesso favor checar usuario e senha', 'danger')
    return render_template('Login.html', title='Login', form=form)

@app.route("/Cadastro", methods=['GET', 'POST'])
def Cadastro():
    form = FormularioDeRegistro()
    if form.validate_on_submit():
        senha_hashed = bcrypt.generate_password_hash(form.Senha.data).decode('utf-8')
        user= UsuarioDB(UsernameDB=form.Usuario.data,NomeDaEmpresaDB= form.NomeDaEmpresa.data,ComercioDB= form.Comercio.data,
                        EmailDB=form.Email.data, PasswordDB= senha_hashed)
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

@app.route("/SegundaJanela", methods=['GET', 'POST'])
@login_required
def SegundaJanela():
    form = DadosEssenciais(request.form)
    if form.validate_on_submit():
        Info = Dado(MarcaDB= form.Marca.data, ModeloDB= form.Modelo.data,VersaoDoMotorDB= form.VersaoDoMotor.data,TipoDeCombustivelDB= form.TipoDeCombustivel.data, 
                    AnoDB= form.Ano.data,QuilometragemDB= form.Quilometragem.data,
                    PrecoDB= form.Preco.data, CorDB= form.Cor.data, 
                    LocalidadeDB= form.Localidade.data,NomeDaEmitente=current_user.NomeDaEmpresaDB,user_id= current_user.id)
        db.session.add(Info)
        db.session.commit()
        flash(f'Seus dados foram inseridos com sucesso!', 'success')
        return render_template("SegundaJanela.html", title = "SegundaJanela",form=form)
    return render_template("SegundaJanela.html", title = "SegundaJanela",form=form)

@app.route("/TerceiraJanela")
def TerceiraJanela():
    TabelaTitulo = ("Marca", "Modelo",'Motor','Combustivel', "Ano", "Quilometragem" , "Preço" , "Cor" , "Local"  )
    contador= Dado.query.filter_by(NomeDaEmitente = current_user.NomeDaEmpresaDB).count()
    faltante= 5-contador
    if contador is None or contador < 5:
        return render_template("TerceiraJanelaSemDados.html", title = "TerceiraJanela",contador= contador, faltante= faltante)
    else:
        return render_template("TerceiraJanela.html", title = "TerceiraJanela", TabelaTitulo =TabelaTitulo,Query=Dado.query.filter_by(NomeDaEmitente = current_user.NomeDaEmpresaDB).order_by(Dado.id.desc()).limit(10).all())
    return render_template("TerceiraJanelaSemDados.html", title = "TerceiraJanela")

@app.route("/Logout")
def Logout():
    logout_user()
    return redirect(url_for('HomePage'))   

@app.route("/ContaEmpresa", methods=['GET', 'POST'])
@login_required
def ContaEmpresa():
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


def enviar_email_reset(user):
    token = user.get_reset_token()
    msg = Message('Reset de Email',sender='ivgnoreply@gmail.com', recipients= [user.EmailDB])
    msg.body =   f''' 

Para resetar sua senha, visite o link a seguir:
Se você não fez esse pedido então simplesmente ignore esse E-mail. 
Caso você o tenha feito então só clicar no link abaixo


{url_for('Reset_token', token= token, _external= True)}


Caso você tenha problemas favor nos contatar pelos contatos expostos no site.
'''
    mail.send(msg)

@app.route("/ResetSenha", methods=['GET', 'POST'])
def ResetSenha():
    if current_user.is_authenticated:
        return redirect(url_for('HomePage'))
    form = RequisitarReset()
    if form.validate_on_submit():
        user=UsuarioDB.query.filter_by(EmailDB= form.Email.data).first()  
        enviar_email_reset(user)
        flash(' Um email foi enviado com instruções.', 'info')  
        return redirect(url_for('Login'))
    return render_template('ResetPedido.html', title = 'Resetar senha',form = form)


@app.route("/ResetSenha/<token>", methods=['GET', 'POST'])
def Reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('HomePage'))
    user=UsuarioDB.verify_reset_token(token)
    if user is None:
        flash(' Esse token não é mais valído', ' warning')
        return redirect(url_for('ResetSenha'))
    form = ResetSenhaForm()
    if form.validate_on_submit():
        senha_hashed = bcrypt.generate_password_hash(form.Senha.data).decode('utf-8')
        user.PasswordDB = senha_hashed
        db.session.commit()
        flash(f'Sua senha foi resetada!', 'success')
        return redirect(url_for('Login'))
    return render_template('ResetToken.html', title = 'Resetar senha',form = form)