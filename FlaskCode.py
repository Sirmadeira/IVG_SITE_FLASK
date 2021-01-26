
import os
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required,UserMixin
from flask_wtf  import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo ,Email, ValidationError
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Mail, Message


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'Login'
login_manager.login_message_category = "info"
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = '587'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail= Mail(app)

class UsuarioDB(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    UsernameDB = db.Column(db.String(20), unique=True, nullable=False)
    EmailDB = db.Column(db.String(120), unique=True, nullable=False)    
    PasswordDB = db.Column(db.String(60), nullable=False)
    NomeDaEmpresaDB= db.Column(db.String(60),unique= True,nullable= False)
    SetorDeAtuaçãoDB= db.Column(db.String(60),unique= False,nullable= False)
    LocalidadeDB=db.Column(db.String(40),nullable= False)
    DadosEmpresa=db.relationship('Dados',backref='author',lazy= "dynamic")

    def get_reset_token(self,expires_sec=1800):
        s= Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'Usuario_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s= Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['Usuario_id']
        except:
            return None
        return UsuarioDB.query.get()

    def __repr__(self):
        return f"User('{self.UsernameDB}', '{self.EmailDB}')"

class Dados(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    MarcaDB=db.Column(db.String(40),unique= True,nullable= False)
    ModeloDB=db.Column(db.String(120),nullable= False)
    VersãoDB=db.Column(db.String(120),nullable= False)
    AnoDB=db.Column(db.Integer,nullable= False)
    QuilomDB=db.Column(db.Integer)
    PrecoDB=db.Column(db.Integer,nullable= False)
    CorDB=db.Column(db.String(20),nullable= False)
    user_id= db.Column(db.Integer, db.ForeignKey('usuariodb.id'), nullable= False)

    def __repr__(self):
        return f"User('{self.MarcaDB}', '{self.ModeloDB}')"


@login_manager.user_loader
def load_user(Usuario_id):
    return UsuarioDB.query.get(int(Usuario_id))

class FormularioDeRegistro(FlaskForm):
    Usuario =StringField('Usuário', 
                        validators = [DataRequired(),Length(min= 2, max=20)])

    NomeDaEmpresa= StringField('Favor informar o nome da sua empresa.',
                        validators=[DataRequired(),Length(min=2, max =30)])

    SetorDeAtuação= StringField('Favor informar seu setor. Exemplo: Revendedora de carro.',
                        validators=[DataRequired(),Length(min=5,max=30)])

    Localidade= StringField('Favor informar cidade onde fica a sede.',
                        validators=[DataRequired(),Length(min=5,max=30)])   

    Email = StringField('Email empresarial',
                        validators=[DataRequired(), Email()])

    Senha= PasswordField('Senha',
                        validators=[DataRequired(),Length(min=5,max=20)])

    ConfirmarSenha= PasswordField('Confirme Senha',
                        validators=[DataRequired(),Length(min=5,max=20), EqualTo('Senha')])

    Confirma=SubmitField('Cadastre-se')

    def validate_Usuario(self, Usuario):
        user = UsuarioDB.query.filter_by(UsernameDB = Usuario.data).first()
        if user:
            raise ValidationError('Esse usuario já existe por favor inserir novo')
    def validate_Email(self, Email):
        user = UsuarioDB.query.filter_by(EmailDB = Email.data).first()
        if user:
            raise ValidationError('Esse email já existe por favor inserir novo')

    def validate_NomeDaEmpresa(self,NomeDaEmpresa):
        user = UsuarioDB.query.filter_by(NomeDaEmpresaDB = NomeDaEmpresa.data).first()
        if user:
            raise ValidationError('Essa empresa já está cadastrada')

class FormularioDeLogin(FlaskForm):
    Usuario =StringField('Usuario', 
                        validators = [DataRequired(),Length(min= 2, max=20)]) 

    Email = StringField('Email',
                        validators=[DataRequired(), Email()])
    Lembrete= BooleanField("Lembre-se de mim")

    Senha= PasswordField('Senha',
                        validators=[DataRequired(),Length(min=5,max=20)])

    Entrar=SubmitField('Entre')

class AtualizarRegistro(FlaskForm):
    Usuario =StringField('Usuario', 
                        validators = [DataRequired(),Length(min= 2, max=20)]) 

    Email = StringField('Email',
                        validators=[DataRequired(), Email()])   

    Confirma=SubmitField('Atualizar')

    def validate_Usuario(self, Usuario):
        if Usuario.data != current_user.UsernameDB:
            user = UsuarioDB.query.filter_by(UsernameDB = Usuario.data).first()
            if user:
                raise ValidationError('Esse usuario já existe por favor inserir novo')

    def validate_Email(self, Email):
        if Email.data != current_user.EmailDB:
            user = UsuarioDB.query.filter_by(EmailDB = Email.data).first()
            if user:
                raise ValidationError('Esse email já existe por favor inserir novo')

class RequisitarReset(FlaskForm):
    Email = StringField('Email',
                        validators=[DataRequired(), Email()]) 

    Confirma=SubmitField('Requisitar reset de senha')

    def validate_Email(self, Email):
        user = UsuarioDB.query.filter_by(EmailDB = Email.data).first()
        if user is None:
            raise ValidationError('Não existe conta com esse E-mail.')

class ResetSenha(FlaskForm):
    Senha= PasswordField('Senha',
                    validators=[DataRequired(),Length(min=5,max=20)])

    ConfirmarSenha= PasswordField('Confirme Senha',
                    validators=[DataRequired(),Length(min=5,max=20), EqualTo('Senha')])

    Confirma=SubmitField('Resetar senha')

class DadosEssenciais(FlaskForm):
    Marca= StringField('Marca do carro')

    Modelo= StringField('Modelo do carro')

    Versao= StringField('Versão do carro')

    Ano= IntegerField()

    Kilometragem= IntegerField()

    Preco= IntegerField()

    Cor= StringField('Favor inserir a cor do carro')



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
    	user= UsuarioDB(UsernameDB=form.Usuario.data, EmailDB=form.Email.data, PasswordDB= senha_hashed, 
                        NomeDaEmpresaDB= form.NomeDaEmpresa.data, 
                        SetorDeAtuaçãoDB=form.SetorDeAtuação.data,
                        LocalidadeDB= form.Localidade.data)
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
@login_required
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


def enviar_email_reset(user): # LEMBRAR DE CRIAR EMAIL NOREPLY
    token = user.get_reset_token()
    msg = Message('Reset de senha',sender='noreplyIVG@gmail.com', recipients= [user.EmailDB])
    msg.body = f''' Para resetar sua senha, visite o link a seguir:
{url_for('Reset_token', token= token, _external= True)}

Se você não fez esse pedido então simplesmente ignore esse E-mail   
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
    user =UsuarioDB.verify_reset_token(token)
    if form.validate_on_submit():
        senha_hashed = bcrypt.generate_password_hash(form.Senha.data).decode('utf-8')
        user.Senha= senha_hashed
        db.session.commit()
        flash(f'Sua senha foi resetada!', 'success')
        return redirect(url_for('Login'))
    if user is None:
        flash(' Esse token não é mais valído', ' warning')
        return redirect(url_for('ResetSenha'))
    form = ResetSenha()

    return render_template('ResetToken.html', title = 'Resetar senha',form = form)




if __name__ == "__main__":
	app.run(debug=True)