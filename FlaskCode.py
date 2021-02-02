
import os
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required,UserMixin
from flask_wtf  import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo ,Email, ValidationError, NumberRange
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
    __tablename__= "UsuarioDB"
    id = db.Column(db.Integer, primary_key=True)
    UsernameDB = db.Column(db.String(20), unique=True, nullable=False)
    EmailDB = db.Column(db.String(120), unique=True, nullable=False)    
    PasswordDB = db.Column(db.String(60), nullable=False)
    NomeDaEmpresaDB= db.Column(db.String(60),unique= True,nullable= False)
    Dados=db.relationship('Dado',backref= 'UsuarioDB', lazy= True)


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

class Dado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    LocalidadeDB=db.Column(db.String(40),nullable= False)
    MarcaDB=db.Column(db.String(40),nullable= False)
    ModeloDB=db.Column(db.String(120),nullable= False)
    AnoDB=db.Column(db.Integer,nullable= False)
    QuilometragemDB=db.Column(db.Integer)
    PrecoDB=db.Column(db.Integer,nullable= False)
    CorDB=db.Column(db.String(20),nullable= False)
    user_id=db.Column(db.Integer, db.ForeignKey('UsuarioDB.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.MarcaDB}', '{self.ModeloDB}', '{self.user_id}')"



class FormularioDeRegistro(FlaskForm):
    Usuario =StringField('Usuário', 
                        validators = [DataRequired(message= 'Favor inserir Usuário '),Length(min= 5, max=20, message= 'Entre 5 a 20 letras')])

    NomeDaEmpresa= StringField('Favor informar o nome da sua empresa.',
                        validators=[DataRequired(message= 'Favor inserir nome da empresa '),Length(min=2, max =30,message= 'Entre 5 a 30 letras')])  

    Email = StringField('Email empresarial',
                        validators=[DataRequired(message= 'Favor inserir local'), Email('Formato de e-mail inválido')])

    Senha= PasswordField('Senha',
                        validators=[DataRequired(message= 'Insira uma senha'),Length(min=5,max=20, message= ' Senha entre 5 a 20 caracteres')])

    ConfirmarSenha= PasswordField('Confirme Senha',
                        validators=[DataRequired(message= 'Confirme sua senha'),Length(min=5,max=20), EqualTo('Senha', message= 'Este campo tem que ser igual ao anterior')])

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
                        validators = [DataRequired(message='Favor inserir o seu nome'),Length(min= 2, max=20, message='Favor manter o formato entre 2 e 20' )]) 

    Email = StringField('Email',
                        validators=[DataRequired(message='Favor inserir o seu nome'), Email(message='Email inválido')])

    Lembrete= BooleanField("Lembre-se de mim")

    Senha= PasswordField('Senha',
                        validators=[DataRequired(message='Favor inserir o seu nome'),Length(min=5,max=20,message='Minimo entre 2 e 20 caracteres' )])

    Entrar=SubmitField('Entre')

class AtualizarRegistro(FlaskForm):
    Usuario =StringField('Usuario', 
                        validators = [DataRequired(message='Favor inserir o seu nome'),Length(min= 2, max=20,message='Favor manter o formato entre 2 e 20')]) 

    Email = StringField('Email',
                        validators=[DataRequired(message='Favor inserir o seu nome'), Email(message='Email inválido')])   

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
                        validators=[DataRequired(message='Favor inserir o seu Email'), Email(message='Email inválido')]) 

    Confirma=SubmitField('Requisitar reset de senha')

    def validate_Email(self, Email):
        user = UsuarioDB.query.filter_by(EmailDB = Email.data).first()
        if user is None:
            raise ValidationError('Não existe conta com esse E-mail.')

class ResetSenha(FlaskForm):
    Senha= PasswordField('Senha',
                    validators=[DataRequired('Favor inserir nova senha'),Length(min=5,max=20,message=' Senha tem que ter entre 5 e 20 caracteres')])

    ConfirmarSenha= PasswordField('Confirme Senha',
                    validators=[DataRequired('Favor confirmar senha'),Length(min=5,max=20,message='Senha tem que ter entre 5 e 20 caracteres'), EqualTo('Senha', message= 'Tem que ser igual a senha')])

    Confirma=SubmitField('Resetar senha')

class DadosEssenciais(FlaskForm):
    
    Marca = StringField('Marca',
                        validators=[DataRequired()])

    Modelo = StringField('Modelo',
                        validators=[DataRequired()])

    Ano = IntegerField('Ano',
                        validators=[NumberRange(max=2021)])

    Quilometragem = IntegerField('Quilometragem',
                        validators=[NumberRange(min=0, max=10000)])

    Preco = IntegerField('Preço',
                        validators=[NumberRange(min=0, max=10000)])

    Cor = StringField('Favor inserir a cor do carro',
                        validators=[DataRequired()])

    Localidade= StringField('Favor informar cidade em que foi feito a venda',
                        validators=[DataRequired(message= 'Favor inserir local'),Length(min=5,max=30,message='Cidade inválida')])

    Confirma=SubmitField('Confirmar inserção')

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
            login_user(Usuario,remember=form.Lembrete.data)
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
    	user= UsuarioDB(UsernameDB=form.Usuario.data,NomeDaEmpresaDB= form.NomeDaEmpresa.data,
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
    form = DadosEssenciais()
    if form.validate_on_submit():
        Info = Dado(MarcaDB= form.Marca.data, ModeloDB= form.Modelo.data, AnoDB= form.Ano.data,QuilometragemDB= form.Quilometragem.data,
                    PrecoDB= form.Preco.data, CorDB= form.Cor.data, 
                    LocalidadeDB= form.Localidade.data, user_id=current_user.id)
        db.session.add(Info)
        db.session.commit()
        flash(f'Seus dados foram inseridos com sucesso!', 'success')
        return render_template("SegundaJanela.html", title = "SegundaJanela",form=form)
    return render_template("SegundaJanela.html", title = "SegundaJanela",form= form)
	
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
    msg = Message('Reset de senha',sender='IVGDONTREPLY@outlook.com', recipients= [user.EmailDB])
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