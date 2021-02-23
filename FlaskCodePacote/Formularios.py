from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField
from wtforms.validators import InputRequired, Length, EqualTo ,Email, ValidationError, NumberRange, AnyOf, Regexp
from FlaskCodePacote.Modelos import UsuarioDB, Dado


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

    MarcasGarantia = ("Acura", "Agrale","Alfo Romeo","Am Gen","Asia motors","ASTON MARTIN","Audi","Baby","BMW",
    "BRM","BUGRE","Cadillac","CBT Jipe","CHANA","CHANGAN","CHERY","Chrysler","Citroën",
    "Cross Lander","Daewoo","Daihatsu","Dodge","EFFA","Engesa","Envemo","Ferrari","Fiat",
    "Fibravan","Ford","FOTON","Fyber","GEELY","GM CHEVROLET","GREAT WALL","Gurgel","HAFEI",
    "HITECH ELECTRIC","HONDA","HYUNDAY","ISUZU","IVECO","JAC","Jaguar","Jeep","JINBEI","JPX",
    "Kia Motors","Lada","Lamborghini","Land Rover","Lexus","LIFAN","LOBINI","Lotus","Mahindra",
    "Maserati","Matra","Mazda","Mclaren","Mercedez-Benz","Mercury","MG","MINI","Mitsubishi","Miura",
    "Nissan","Peugeot","Plymouth","Pontiac","Porsche","RAM","RELY","Renault","Rolls-Royce","Rover",
    "Saab","Saturn","Seat","SHINERAY","smart","SSANGYONG","Subaru","Suzuki","TAC","Toyota","Troller","Volvo","VW-VOLKSWAGEN","Wake","Walk")

    Localidades= ("Limeira", "Piracicaba","limeira", "piracicaba")

    CoresGarantia = ("Amarelo","Azul","Bege","Branco","Bronze","Cinza","Dourado","Indefinida","Laranja","Marrom","Prata","Preto",
                    "Rosa","Roxo","Verde","Vermelho","Vinho")

    Combustiveis= ('Gasolina','Etanol','GNV','Diesel','Flex')
    
    Marca = StringField('Marca',
                        validators=[InputRequired(message='Favor inserir uma Marca valida'), AnyOf(MarcasGarantia, message= 
                                    '''
                                    Trabalhamos com as seguintes marcas, escrever igual a maneira abaixo:
                                    Acura/Agrale/Alfo Romeo/Am Gen/Asia motors/ASTON MARTIN/Audi/Baby/BMW/BRM/BUGRE/Cadillac/
                                    CBT Jipe/CHANA/CHANGAN/CHERY/Chrysler/Citroën/Cross Lander/Daewoo/Daihatsu/
                                    Dodge/EFFA/Engesa/Envemo/Ferrari/Fiat/Fibravan/Ford/FOTON/Fyber/GEELY/GM CHEVROLET/
                                    GREAT WALL/Gurgel/HAFEI/HITECH ELECTRIC/HONDA/HYUNDAY/ISUZU/IVECO/JAC/Jaguar/Jeep/JINBEI/JPX/
                                    Kia Motors/Lada/Lamborghini/Land Rover/Lexus/LIFAN/LOBINI/Lotus/Mahindra/Maserati/Matra/Mazda/
                                    Mclaren/Mercedez-Benz/Mercury/MG/MINI/Mitsubishi/Miura/Nissan/Peugeot/Plymouth/Pontiac/Porsche/
                                    RAM/RELY/Renault/Rolls-Royce/Rover/Saab/Saturn/Seat/SHINERAY/smart/SSANGYONG/Subaru/Suzuki/
                                    TAC/Toyota/Troller/Volvo/VW-VOLKSWAGEN/Wake/Walk''' )])
    
    Modelo = StringField('Modelo',
                        validators=[InputRequired(message='Favor inserir um modelo valido')])

    VersaoDoMotor = StringField('Motor',
                        validators=[InputRequired(message='Favor inserir um motor valido')])

    TipoDeCombustivel = StringField('Combustivél',
                        validators=[InputRequired(message='Favor inserir um modelo valido'), AnyOf(Combustiveis, message= f' Os combustiveis aceitos são: {Combustiveis}' )])

    Ano = FloatField('Ano',
                        validators=[NumberRange(min= 1960, max=2021, message = 'Somente por carros acima do ano 1960')])

    Quilometragem = IntegerField('Quilometragem',
                        validators=[NumberRange(min=0, max=9999999, message= "Não existe km negativa ou essa km e muita alta")])

    Preco = FloatField('Preço',
                        validators=[NumberRange(min=1000, max=9999999, message = 'Somente por vendas acima de mil reais.')])

    Cor = StringField('Cor',
                        validators=[InputRequired(message= 'Favor inserir cor do carro'), AnyOf(CoresGarantia, message= f'''Caso a cor não seja aceita e porque ela é muito atípica. 
                        Ou não é constatada no banco de cores.
                        Favor inserir indefinida no campo nesse caso
                        As cores aceitas são: {CoresGarantia}''')])

    Localidade= StringField('Local da venda',
                        validators=[InputRequired(message= 'Favor inserir local'),AnyOf(Localidades, message= 'Atualmente só trabalhamos com vendas realizadas em Limeira e Piracicaba')])

    Confirma=SubmitField('Confirmar inserção')