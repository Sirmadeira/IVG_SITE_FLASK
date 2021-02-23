from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required,UserMixin
from flask_wtf  import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextField, FloatField
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
app.config['MAIL_USERNAME'] = 'ivgnoreply@gmail.com'
app.config['MAIL_PASSWORD'] = 'MO517364@@12'
mail= Mail(app)


@login_manager.user_loader
def load_user(user_id):
    return UsuarioDB.query.get(int(user_id))


class UsuarioDB(db.Model,UserMixin):
    __tablename__= "UsuarioDB"
    id = db.Column(db.Integer, primary_key=True)
    UsernameDB = db.Column(db.String(20), unique=True, nullable=False)
    EmailDB = db.Column(db.String(40), unique=True, nullable=False)    
    PasswordDB = db.Column(db.String(120), nullable=False)
    NomeDaEmpresaDB= db.Column(db.String(30),unique= True,nullable= False)
    ComercioDB=db.Column(db.String(30),nullable= False)
    Dados=db.relationship('Dado',backref= 'UsuarioDB',lazy= True)


    def get_reset_token(self, expires_sec=1800):
        s= Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s= Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return UsuarioDB.query.get(user_id)

    def __repr__(self):
        return f"User('{self.UsernameDB}', '{self.EmailDB}')"

class Dado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    LocalidadeDB=db.Column(db.String(40),nullable= False)
    MarcaDB=db.Column(db.String(40),nullable= False)
    ModeloDB=db.Column(db.String(120),nullable= False)
    VersaoDoMotorDB=db.Column(db.String(120),nullable= False)
    TipoDeCombustivelDB=db.Column(db.String(120),nullable= False)
    AnoDB=db.Column(db.Integer,nullable= False)
    QuilometragemDB=db.Column(db.Float)
    PrecoDB=db.Column(db.Float,nullable= False)
    CorDB=db.Column(db.String(20),nullable= False)
    NomeDaEmitente= db.Column(db.String(30),nullable= False)
    user_id = db.Column(db.Integer, db.ForeignKey('UsuarioDB.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.MarcaDB}', '{self.ModeloDB}')"



class FormularioDeRegistro(FlaskForm):


    Usuario =StringField('Usuário', 
                        validators = [InputRequired(message= 'Favor inserir Usuário '),Length(min= 5, max=20, message= 'Entre 4 a 20 letras')])

    NomeDaEmpresa= StringField('Favor informar o nome da sua empresa.',
                        validators=[InputRequired(message= 'Favor inserir nome da empresa '),Length(min=2, max =30,message= 'Entre 5 a 30 letras')])

    Comercio= StringField('Favor informar o setor de atuação da sua empresa',
                        validators=[InputRequired(message= 'Favor inserir tipo de comercio '),AnyOf('Revendedora de carro', message= 'Atualmente só trabalhamos com: Revendedora de carro, copie e cole o exemplo caso haja erro.')])   

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
                        validators = [InputRequired(message='Favor inserir o seu Usuário')]) 

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

class ResetSenhaForm(FlaskForm):

    Senha = PasswordField('Nova senha',
                    validators=[InputRequired(message= 'Insira uma senha'),Regexp('^(?:(?=.*[a-z])(?:(?=.*[A-Z])(?=.*[\d\W])|(?=.*\W)(?=.*\d))|(?=.*\W)(?=.*[A-Z])(?=.*\d)).{8,}$', message= 'Sua senha precisa ter 8 caracteres e pelo menos obedecer 3 das 4 condições, ter letra maiúscula minúscula, ter número e/ou caracteres especiais.')])

    ConfirmarSenha= PasswordField('Confirme Senha',
                    validators=[InputRequired('Favor confirmar senha'), EqualTo('Senha', message= 'Tem que ser igual a senha')])

    Confirma=SubmitField('Resetar senha')



class DadosEssenciais(FlaskForm):

    MarcasGarantia = ("ACURA", "AGRALE","AlFO ROMEO","AM GEN","ASIA MOTORS","ASTON MARTIN","AUDI","BABY","BMW",
    "BRM","BUGRE","CADILLAC","CBT JIPE","CHANA","CHANGAN","CHERY","CHRYSLER","CITROËN","CITROEN",
    "CROSS LANDER","DAEWOO","DAIHATSU","DODGE","EFFA","ENGESA","ENVEMO","FERRARI","FIAT",
    "FIBRAVAN","FORD","FOTON","FYBER","GEELY","GM CHEVROLET","GREAT WALL","GURGEL","HAFEI",
    "HITECH ELECTRIC","HONDA","HYUNDAY","ISUZU","IVECO","JAC","JAGUAR","JEEP","JINBEI","JPX",
    "KIA MOTORS","LADA","LAMBORGHINI","LAND ROVER","LEXUS","LIFAN","LOBINI","LOTUS","MAHINDRA",
    "MASERATI","MATRA","MAZDA","MCLAREN","MERCEDEZ-BENZ","MERCURY","MG","MINI","MITSUBISHI","MIURA",
    "NISSAN","PEUGEOT","PLYMOUTH","PONTIAC","PORSCHE","RAM","RELY","RENAULT","ROLLS-ROYCE","ROVER",
    "SAAB","SATURN","SEAT","SHINERAY","SMART","SSANGYONG","SUBARU","SUZUKI","TAC","TOYOTA","TROLLER","VOLVO","VW-VOLKSWAGEN","WAKE","WALK")

    Localidades= ("LIMEIRA", "PIRACICABA")

    CoresGarantia = ("AMARELO","AZUL","BEGE","BRANCO","BRONZE","CINZA","DOURADO","INDEFINIDA","LARANJA","MARROM","PRATA","PRETO",
                    "ROSA","ROXO","VERDE","VERMELHO","VINHO")

    Combustiveis= ('GASOLINA','ETANOL','GNV','DISEL','FLEX')
    
    Marca = StringField('MARCA',
                        validators=[InputRequired(message='Favor inserir uma Marca valida'), AnyOf(MarcasGarantia, message= 
                                    '''
                                    Trabalhamos com as seguintes marcas, escreva da maneira abaixo:
                                    Acura/Agrale/Alfo Romeo/Am Gen/Asia motors/ASTON MARTIN/Audi/Baby/BMW/BRM/BUGRE/Cadillac/
                                    CBT Jipe/CHANA/CHANGAN/CHERY/Chrysler/Citroën/Cross Lander/Daewoo/Daihatsu/
                                    Dodge/EFFA/Engesa/Envemo/Ferrari/Fiat/Fibravan/Ford/FOTON/Fyber/GEELY/GM CHEVROLET/
                                    GREAT WALL/Gurgel/HAFEI/HITECH ELECTRIC/HONDA/HYUNDAY/ISUZU/IVECO/JAC/Jaguar/Jeep/JINBEI/JPX/
                                    Kia Motors/Lada/Lamborghini/Land Rover/Lexus/LIFAN/LOBINI/Lotus/Mahindra/Maserati/Matra/Mazda/
                                    Mclaren/Mercedez-Benz/Mercury/MG/MINI/Mitsubishi/Miura/Nissan/Peugeot/Plymouth/Pontiac/Porsche/RAM/
                                    RELY/Renault/Rolls-Royce/Rover/Saab/Saturn/Seat/SHINERAY/smart/SSANGYONG/Subaru/Suzuki/TAC/Toyota/Troller/
                                    Volvo/VW-VOLKSWAGEN/Wake/Walk''' )])
    
    Modelo = StringField('MODELO, FAVOR OLHAR NO RENAVAN',
                        validators=[InputRequired(message='Favor inserir um modelo valido')])

    VersaoDoMotor = StringField('MOTOR',
                        validators=[InputRequired(message='Favor inserir um motor valido')])

    TipoDeCombustivel = StringField('Tipo de combustível',
                        validators=[InputRequired(message='Favor inserir um modelo valido'), AnyOf(Combustiveis, message=' Os combustiveis aceitos são: Gasolina/Etanol/GNV/Diesel/Flex' )])

    Ano = FloatField('ANO',
                        validators=[NumberRange(min= 1960, max=2021, message = 'Somente por carros acima do ano 1960')])

    Quilometragem = IntegerField('Quilometragem',
                        validators=[NumberRange(min=0, max=9999999, message= "Não existe km negativa ou essa km e muita alta")])

    Preco = FloatField('PREÇO',
                        validators=[NumberRange(min=1000, max=9999999, message = 'Somente por vendas acima de mil reais.')])

    Cor = StringField('COR',
                        validators=[InputRequired(message= 'Favor inserir cor do carro'), AnyOf(CoresGarantia, message= '''Caso a cor não seja aceita e porque ela é muito atípica. 
                        Ou não é constatada no banco de cores da web motors.
                        Favor inserir indefinida no campo nesse caso''')])

    Localidade= StringField('LOCAL DA VENDA',
                        validators=[InputRequired(message= 'Favor inserir local'),AnyOf(Localidades, message= 'Atualmente só trabalhamos com vendas realizadas em Limeira e Piracicaba')])

    Confirma=SubmitField('Confirmar inserção')

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

if __name__ == "__main__":
    app.run(debug=True)