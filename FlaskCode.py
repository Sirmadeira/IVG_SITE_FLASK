import os
from flask import Flask, render_template, url_for, flash, redirect, request, Response, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required,UserMixin
from flask_wtf  import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextField
from wtforms.validators import InputRequired, Length, EqualTo ,Email, ValidationError, NumberRange, AnyOf, Regexp
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
    EmailDB = db.Column(db.String(40), unique=True, nullable=False)    
    PasswordDB = db.Column(db.String(120), nullable=False)
    NomeDaEmpresaDB= db.Column(db.String(30),unique= True,nullable= False)
    Nomes=db.relationship('Dado',backref= 'UsuarioDB',lazy= True)


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
    nome_id=db.Column(db.String(30),db.ForeignKey('UsuarioDB.NomeDaEmpresaDB'),nullable= False)

    def __repr__(self):
        return f"User('{self.MarcaDB}', '{self.ModeloDB}')"



class FormularioDeRegistro(FlaskForm):
    Usuario =StringField('Usuário', 
                        validators = [InputRequired(message= 'Favor inserir Usuário '),Length(min= 5, max=20, message= 'Entre 4 a 20 letras')])

    NomeDaEmpresa= StringField('Favor informar o nome da sua empresa.',
                        validators=[InputRequired(message= 'Favor inserir nome da empresa '),Length(min=2, max =30,message= 'Entre 5 a 30 letras')])  

    Email = StringField('Email empresarial',
                        validators=[InputRequired(message= 'Favor inserir Email'), Email('Formato de e-mail inválido')])

    Senha= PasswordField('Senha',
                        validators=[InputRequired(message= 'Insira uma senha'),Regexp('^(?:(?=.*[a-z])(?:(?=.*[A-Z])(?=.*[\d\W])|(?=.*\W)(?=.*\d))|(?=.*\W)(?=.*[A-Z])(?=.*\d)).{8,}$', message= 'Sua senha precisa ter 8 caracteres e pelo menos obedecer 3 das 4 condições, ter letra maiúscula minúscula, ter número e/ou caracteres especiais.')])

    ConfirmarSenha= PasswordField('Confirme Senha',
                        validators=[InputRequired(message= 'Confirme sua senha'),EqualTo('Senha', message= 'Este campo tem que ser igual ao de senha')])

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
                        validators = [InputRequired(message='Favor inserir o seu Usuário')]) 

    Email = StringField('Email',
                        validators=[InputRequired(message='Favor inserir o seu E-mail'), Email(message='Email inválido')])

    Lembrete= BooleanField("Lembre-se de mim")

    Senha= PasswordField('Senha',
                        validators=[InputRequired(message='Favor inserir a sua senha')])

    Entrar=SubmitField('Entre')

class AtualizarRegistro(FlaskForm):
    Usuario =StringField('Usuario', 
                        validators = [InputRequired(message='Favor inserir o seu Usuário'),Length(min= 4, max=20,message='Favor manter o formato entre 4 e 20 caracteres')]) 

    Email = StringField('Email',
                        validators=[InputRequired(message='Favor inserir o seu Email'), Email(message='Email em formato não aceitável')])   

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
                        validators=[InputRequired(message='Favor inserir o seu Email'), Email(message='Email inválido')]) 

    Confirma=SubmitField('Requisitar reset de senha')

    def validate_Email(self, Email):
        user = UsuarioDB.query.filter_by(EmailDB = Email.data).first()
        if user is None:
            raise ValidationError('Não existe conta com esse E-mail.')

class ResetSenha(FlaskForm):
    Senha= PasswordField('Senha',
                    validators=[InputRequired('Favor inserir nova senha'),Length(min=5,max=20,message=' Senha tem que ter entre 5 e 20 caracteres')])

    ConfirmarSenha= PasswordField('Confirme Senha',
                    validators=[InputRequired('Favor confirmar senha'),Length(min=5,max=20,message='Senha tem que ter entre 5 e 20 caracteres'), EqualTo('Senha', message= 'Tem que ser igual a senha')])

    Confirma=SubmitField('Resetar senha')



class DadosEssenciais(FlaskForm):

    MarcasGarantia = ("Acura", "Agrale","Alfo Romeo","Am Gen","Asia motors","ASTON MARTIN","Audi","Baby","BMW",
    "BRM","BUGRE","Cadillac","CBT Jipe","CHANA","CHANGAN","CHERY","Chrysler","Citroën",
    "Cross Lander","Daewoo","Daihatsu","Dodge","EFFA","Engesa","Envemo","Ferrari","Fiat",
    "Fibravan","Ford","FOTON","Fyber","GEELY","GM CHEVROLET","GREAT WALL","Gurgel","HAFEI",
    "HITECH ELECTRIC","HONDA","HYUNDAY","ISUZU","IVECO","JAC","Jaguar","Jeep","JINBEI","JPX",
    "Kia Motors","Lada","Lamborghini","Land Rover","Lexus","LIFAN","LOBINI","Lotus","Mahindra",
    "Maserati","Matra","Mazda","Mclaren","Mercedez-Benz","Mercury","MG","MINI","Mitsubishi","Miura",
    "Nissan","Peugeot","Plymouth","Pontiac","Porsche","RAM","RELY","Renault","Rolls-Royce","Rover",
    "Saab","Saturn","Seat","SHINERAY","smart","SSANGYONG","Subaru","Suzuki","TAC","Toyota","Troller","Volvo","VW-VOLKSWAGEN","Wake","Walk")

    Localidades= ("Limeira", "Piracicaba")

    CoresGarantia = ("Amarelo","Azul","Bege","Branco","Bronze","Cinza","Dourado","Indefinida","Laranja","Marrom","Prata","Preto",
                    "Rosa","Roxo","Verde","Vermelho","Vinho")
    
    Marca = StringField('Marca',id= "marca_autocomplete:",
                        validators=[InputRequired(message='Favor inserir uma Marca valida'), AnyOf(MarcasGarantia, message= " Essas são as marcas disponiveis:(Favor escrever de acordo com o mostrado) Acura/Agrale/Alfo Romeo/Am Gen/Asia motors/ASTON MARTIN/Audi/Baby/BMW/BRM/BUGRE/Cadillac/CBT Jipe/CHANA/CHANGAN/CHERY/Chrysler/Citroën/Cross Lander/Daewoo/Daihatsu/Dodge/EFFA/Engesa/Envemo/Ferrari/Fiat/Fibravan/Ford/FOTON/Fyber/GEELY/GM CHEVROLET/GREAT WALL/Gurgel/HAFEI/HITECH ELECTRIC/HONDA/HYUNDAY/ISUZU/IVECO/JAC/Jaguar/Jeep/JINBEI/JPX/Kia Motors/Lada/Lamborghini/Land Rover/Lexus/LIFAN/LOBINI/Lotus/Mahindra/Maserati/Matra/Mazda/Mclaren/Mercedez-Benz/Mercury/MG/MINI/Mitsubishi/Miura/Nissan/Peugeot/Plymouth/Pontiac/Porsche/RAM/RELY/Renault/Rolls-Royce/Rover/Saab/Saturn/Seat/SHINERAY/smart/SSANGYONG/Subaru/Suzuki/TAC/Toyota/Troller/Volvo/VW-VOLKSWAGEN/Wake/Walk" )])
    
    Modelo = StringField('Modelo',
                        validators=[InputRequired(message='Favor inserir um modelo valido')])

    Ano = IntegerField('Ano',
                        validators=[NumberRange(min= 1960, max=2021, message = 'Somente por carros acima do ano 1960')])

    Quilometragem = IntegerField('Quilometragem',
                        validators=[NumberRange(min=0, max=10000000000)])

    Preco = IntegerField('Preço',
                        validators=[NumberRange(min=1000, max=10000000000, message = 'Somente por vendas acima de mil reais.')])

    Cor = StringField('Favor inserir a cor do carro',
                        validators=[InputRequired(message= 'Favor inserir cor do carro'), AnyOf(CoresGarantia, message= 'Favor inserir a cor com a primeira letra maiúscula, caso a cor não seja aceita e porque ela é muito atípica, favor inserir indefinida no campo nesse caso')])

    Localidade= StringField('Favor informar cidade em que foi feito a venda',
                        validators=[InputRequired(message= 'Favor inserir local'),AnyOf(Localidades, message= 'Favor inserir a cidade com a primeira letra maiúscula. Atualmente só trabalhamos com vendas realizadas em Limeira e Piracicaba')])

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

@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    marca = ["Acura",
            "VW-VOLKSWAGEN"]
    print(marca)    
    return Response(json.dumps(marca), mimetype='application/json')

@app.route("/SegundaJanela", methods=['GET', 'POST'])
@login_required
def SegundaJanela():
    form = DadosEssenciais(request.form)
    if form.validate_on_submit():
        Info = Dado(MarcaDB= form.Marca.data, ModeloDB= form.Modelo.data, AnoDB= form.Ano.data,QuilometragemDB= form.Quilometragem.data,
                    PrecoDB= form.Preco.data, CorDB= form.Cor.data, 
                    LocalidadeDB= form.Localidade.data,nome_id=current_user.NomeDaEmpresaDB)
        db.session.add(Info)
        db.session.commit()
        flash(f'Seus dados foram inseridos com sucesso!', 'success')
        return render_template("SegundaJanela.html", title = "SegundaJanela",form=form)
    return render_template("SegundaJanela.html", title = "SegundaJanela",form=form)

@app.route("/TerceiraJanela")
def TerceiraJanela():
    TabelaTitulo = ("Marca", "Modelo", "Ano", "Quilometragem" , "Preço" , "Cor" , "Local"  )

    return render_template("TerceiraJanela.html", title = "TerceiraJanela", TabelaTitulo =TabelaTitulo,Query=Dado.query.filter_by(nome_id = current_user.NomeDaEmpresaDB).order_by(Dado.id.desc()).limit(10).all())

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