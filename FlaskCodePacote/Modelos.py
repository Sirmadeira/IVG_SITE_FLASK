from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from FlaskCodePacote import db, login_manager
from flask_login import  UserMixin
from flask import current_app


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
        s= Serializer(current_app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s= Serializer(current_app.config['SECRET_KEY'])
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
