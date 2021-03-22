
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, AnyOf, NumberRange, ValidationError
from FlaskCodePacote.Modelos import Dado
from FlaskCodePacote.Principal.Utilidades import MeuFloatField, MeuIntegerField



class DadosEssenciais(FlaskForm):
    
    Marca = StringField('Marca', id='marca_autocomplete',
                        validators=[InputRequired(message='Favor inserir uma Marca valida')],render_kw={"placeholder": "Marca do veículo"})
    
    Modelo = StringField('Modelo',id='modelo_autocomplete',
                        validators=[InputRequired(message='Favor inserir um modelo valido')],render_kw={"placeholder": "Modelo do veículo"})

    VersaoDoMotor = StringField('Motor',id='motor_autocomplete',
                        validators=[InputRequired(message='Favor inserir um motor valido')],render_kw={"placeholder": "Versão do motor"})

    TipoDeCombustivel = StringField('Combustivél', id='combustivel_autocomplete',
                        validators=[InputRequired(message='Favor inserir um modelo valido')],render_kw={"placeholder": "Combustivél aceitos"})

    Ano = MeuIntegerField('Ano',
                        validators=[NumberRange(min= 1960, max=2021, message = 'Somente por carros acima do ano 1960')],render_kw={"placeholder": "Ano do veículo"})

    Quilometragem = MeuFloatField('Quilometragem',
                        validators=[NumberRange(min=0, max=9999999, message= "Não existe km negativa ou essa km e muita alta")],render_kw={"placeholder": "KM"})

    Preco = MeuFloatField('Preço',
                        validators=[NumberRange(min=1000, max=9999999, message = 'Somente por vendas acima de mil reais.')],render_kw={"placeholder": "Preço de venda"})

    Lucro= MeuFloatField('Lucro',
                        validators=[InputRequired(message= 'Favor inserir lucro, caso seja venda por 0 como valor')],render_kw={"placeholder": "Lucro sobre a venda"})

    Cor = StringField('Cor',id= 'cor_autocomplete',
                        validators=[InputRequired(message= 'Favor inserir cor do carro')],render_kw={"placeholder": "Cor do veículo"})

    Localidade= StringField('Local da venda',id= 'local_autocomplete',
                        validators=[InputRequired(message= 'Favor inserir local')],render_kw={"placeholder": "Local da venda"})

    Confirma=SubmitField('Confirmar inserção')

    def validate_Marca(self, Marca):
        GarantiaMarca = Dado.query.filter_by(MarcaDB = Marca.data.upper()).first() 
        if GarantiaMarca is None:
            raise ValidationError('''
                                Trabalhamos com as seguintes marcas, escrever igual a maneira abaixo:
                                Acura/Agrale/Alfo Romeo/Am Gen/Asia motors/ASTON MARTIN/Audi/Baby/BMW/BRM/BUGRE/Cadillac/
                                CBT Jipe/CHANA/CHANGAN/CHERY/Chrysler/Citroën/Cross Lander/Daewoo/Daihatsu/
                                Dodge/EFFA/Engesa/Envemo/Ferrari/Fiat/Fibravan/Ford/FOTON/Fyber/GEELY/GM CHEVROLET/
                                GREAT WALL/Gurgel/HAFEI/HITECH ELECTRIC/HONDA/HYUNDAY/ISUZU/IVECO/JAC/Jaguar/Jeep/JINBEI/JPX/
                                Kia Motors/Lada/Lamborghini/Land Rover/Lexus/LIFAN/LOBINI/Lotus/Mahindra/Maserati/Matra/Mazda/
                                Mclaren/Mercedez-Benz/Mercury/MG/MINI/Mitsubishi/Miura/Nissan/Peugeot/Plymouth/Pontiac/Porsche/
                                RAM/RELY/Renault/Rolls-Royce/Rover/Saab/Saturn/Seat/SHINERAY/smart/SSANGYONG/Subaru/Suzuki/
                                TAC/Toyota/Troller/Volvo/VW-VOLKSWAGEN/Wake/Walk''')

    def validate_TipoDeCombustivel(self, TipoDeCombustivel):
        Combustiveis= ('Gasolina','Etanol','GNV','Diesel','Flex')
        GarantiaCombustivel = Dado.query.filter_by(TipoDeCombustivelDB = TipoDeCombustivel.data.upper()).first()
        if GarantiaCombustivel is None:
            raise ValidationError(f'Os combustiveis aceitos são: { Combustiveis }')

    def validate_Cor(self, Cor):
        Cores = ("Amarelo","Azul","Bege","Branco","Bronze","Cinza","Dourado","Indefinida","Laranja","Marrom","Prata","Preto","Rosa","Roxo","Verde","Vermelho","Vinho")
        GarantiaCor = Dado.query.filter_by(CorDB = Cor.data.upper()).first()
        if GarantiaCor is None:
            raise ValidationError(f'''Caso a cor não seja aceita e porque ela é muito atípica. 
                        Ou não é constatada no banco de cores.
                        Favor inserir indefinida no campo nesse caso
                        As cores aceitas são: { Cores }''')

    def validate_Localidade(self, Localidade):
        GarantiaLocalidade = Dado.query.filter_by(LocalidadeDB = Localidade.data.upper()).first()
        if GarantiaLocalidade is None:
            raise ValidationError('Atualmente só trabalhamos com vendas realizadas em Limeira e Piracicaba')