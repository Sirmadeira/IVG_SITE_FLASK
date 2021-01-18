from FlaskCode import db

class UsuariosDB(db.Model):
	id = db.Column(db.Integer, primary_key= True)
	UsuarioDB = db.Column(db.String(20), unique= True, nullable = False)
	EmailDB = db.Column(db.String(120), unique= True, nullable = False)
	SenhaDB = db.Column(db.String(60), nullable = False)


	def __repr__(self):
		return f"UsuariosDB('{self.UsuarioDB}','{self.EmailDB}')"