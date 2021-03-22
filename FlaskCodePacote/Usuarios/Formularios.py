from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError, Regexp, AnyOf
from flask_login import current_user
from FlaskCodePacote.Modelos import UsuarioDB


class FormularioDeRegistro(FlaskForm):

    Usuario =StringField('Usuário', 
                        validators = [InputRequired(message= 'Favor inserir Usuário '),Length(min= 5, max=20, message= 'Entre 4 a 20 letras')],render_kw={"placeholder": "Usuário"})

    NomeDaEmpresa= StringField('Favor informar o nome da sua empresa.',
                        validators=[InputRequired(message= 'Favor inserir nome da empresa '),Length(min=2, max =30,message= 'Entre 5 a 30 letras')],render_kw={"placeholder": "Inserir nome da sua empresa"})

    Comercio= StringField('Favor informar o setor de atuação da sua empresa',
                        validators=[InputRequired(message= 'Favor inserir tipo de comercio '),AnyOf('Revendedora de carro', message= 'Atualmente só trabalhamos com: Revendedora de carro , copie e cole o exemplo caso haja erro.')],render_kw={"placeholder": "Comercio da sua empresa"})   

    Email = StringField('Email empresarial',
                        validators=[InputRequired(message= 'Favor inserir Email'), Email('Formato de e-mail inválido')],render_kw={"placeholder": "Email de contato empresarial"})

    Senha= PasswordField('Senha',
                        validators=[InputRequired(message= 'Insira uma senha'),Regexp('^(?:(?=.*[a-z])(?:(?=.*[A-Z])(?=.*[\d\W])|(?=.*\W)(?=.*\d))|(?=.*\W)(?=.*[A-Z])(?=.*\d)).{8,}$', message= 'Sua senha precisa ter 8 caracteres e pelo menos obedecer 3 das 4 condições, ter letra maiúscula minúscula, ter número e/ou caracteres especiais.')],render_kw={"placeholder": "Senha aviso, precisa ter 8 caracteres com letras maiúsculas minúsculas e caracteres especiais"})

    ConfirmarSenha= PasswordField('Confirme Senha',
                        validators=[InputRequired(message= 'Confirme sua senha'),EqualTo('Senha', message= 'Este campo tem que ser igual ao de senha')],render_kw={"placeholder": "Repita sua senha"})

    RecaptchaCampo= RecaptchaField()

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
    Usuario =StringField('Usuário', 
                        validators = [InputRequired(message='Favor inserir o seu Usuário')],render_kw={"placeholder": "Usuário"}) 

    Email = StringField('Email',
                        validators=[InputRequired(message='Favor inserir o seu E-mail'), Email(message='Email inválido')],render_kw={"placeholder": "Email da sua empresa"})

    Lembrete= BooleanField("Lembre-se de mim")

    Senha= PasswordField('Senha',
                        validators=[InputRequired(message='Favor inserir a sua senha')],render_kw={"placeholder": "Senha"})

    Entrar=SubmitField('Entre')

class AtualizarRegistro(FlaskForm):
    Usuario =StringField('Seu usuário atual', 
                        validators = [InputRequired(message='Favor inserir o seu Usuário')]) 

    Email = StringField('Seu email atual',
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
                        validators=[InputRequired(message='Favor inserir o seu Email'), Email(message='Email inválido')],render_kw={"placeholder": "Favor inserir o email de contato da sua empresa"}) 

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