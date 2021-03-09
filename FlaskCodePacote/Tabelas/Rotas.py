from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint, Response, json, jsonify)
from flask_login import current_user, login_required
from sqlalchemy import func, desc
from FlaskCodePacote import db
from FlaskCodePacote.Modelos import Dado
from FlaskCodePacote.Tabelas.Formularios import DadosEssenciais


Tabelas = Blueprint('Tabelas', __name__)   


@Tabelas.route("/SegundaJanela", methods=['GET', 'POST'])
@login_required
def SegundaJanela():
    form = DadosEssenciais()
    if form.validate_on_submit():
        Info = Dado(MarcaDB= form.Marca.data.upper(), ModeloDB= form.Modelo.data.upper(),VersaoDoMotorDB= form.VersaoDoMotor.data.upper(),TipoDeCombustivelDB= form.TipoDeCombustivel.data.upper(), 
                    AnoDB= form.Ano.data,QuilometragemDB= form.Quilometragem.data,
                    PrecoDB= form.Preco.data, CorDB= form.Cor.data.upper(), 
                    LocalidadeDB= form.Localidade.data.upper(),NomeDaEmitente=current_user.NomeDaEmpresaDB,MargemDeLucroDB = (form.Lucro.data/form.Preco.data)*100,user_id= current_user.id)
        db.session.add(Info)
        db.session.commit()
        flash(f'Seus dados foram inseridos com sucesso!', 'success')
        return render_template("SegundaJanela.html", title = "SegundaJanela",form=form)
    return render_template("SegundaJanela.html", title = "SegundaJanela",form=form)

@Tabelas.route("/TerceiraJanela")
@login_required
def TerceiraJanela():
    PresentePython = '%'
    TituloDadosInserido = ("Marca","Modelo",'Motor','Combustivel', "Ano", "Quilometragem" , "Preço" , "Cor" , "Margem de Lucro" ,"Controle" )
    TituloTop20Modelo=("Marca","Modelo","N.º de vendas")
    TituloTop20Marca=("Marca"," N.º de vendas")
    TituloMargemLucro=('Marca','Modelo','Média de Lucro')
    contador= Dado.query.filter_by(NomeDaEmitente = current_user.NomeDaEmpresaDB).count()
    faltante= 5-contador
    if contador is None or contador < 5:
        return render_template("TerceiraJanelaSemDados.html", title = "TerceiraJanela",contador= contador, faltante= faltante)
    else:
        return render_template("TerceiraJanela.html", title = "TerceiraJanela",PresentePython= PresentePython, 
                                TituloDadosInserido =TituloDadosInserido,Query=Dado.query.filter_by(NomeDaEmitente = current_user.NomeDaEmpresaDB).order_by(Dado.id.desc()).limit(10).all(),
                                TituloTop20Modelo= TituloTop20Modelo, ContadorGrupo= Dado.query.with_entities(Dado.MarcaDB,Dado.ModeloDB,func.count(Dado.ModeloDB).label('total')).group_by(Dado.ModeloDB).order_by(desc('total')).limit(20),
                                TituloTop20Marca=TituloTop20Marca, ContadorGrupo2= Dado.query.with_entities(Dado.MarcaDB,func.count(Dado.MarcaDB).label('total2')).group_by(Dado.MarcaDB).order_by(desc('total2')).limit(20).all(),
                                TituloMargemLucro= TituloMargemLucro, ContadorGrupo3= Dado.query.with_entities(Dado.MarcaDB,Dado.ModeloDB,func.avg(Dado.MargemDeLucroDB).label('media')).group_by(Dado.ModeloDB).order_by(desc('media')).all())

    return render_template("TerceiraJanelaSemDados.html", title = "TerceiraJanela") 

@Tabelas.route('/Deleta/<int:id>')
def Deleta(id):
    deletalinha = Dado.query.get_or_404(id)
    try:
        db.session.delete(deletalinha)
        db.session.commit()
        return redirect(url_for('Tabelas.TerceiraJanela') )
    except:
        return 'Ouve um problema deletando essa linha!'
        
@Tabelas.route('/_AutocompleteMarca', methods=['GET'])
def AutocompleteMarca():
    marca = ['Acura','Agrale','Alfo Romeo','Am Gen','Asia motors','ASTON MARTIN','Audi','Baby','BMW','BRM','BUGRE','Cadillac',
                                'CBT Jipe','CHANA','CHANGAN','CHERY','Chrysler','Citroën','Cross Lander','Daewoo','Daihatsu',
                                'Dodge','EFFA','Engesa','Envemo','Ferrari','Fiat','Fibravan','Ford','FOTON','Fyber','GEELY','GM CHEVROLET',
                                'GREAT WALL','Gurgel','HAFEI','HITECH ELECTRIC','HONDA','HYUNDAY','ISUZU','IVECO','JAC','Jaguar','Jeep','JINBEI','JPX',
                                'Kia Motors','Lada','Lamborghini','Land Rover','Lexus','LIFAN','LOBINI','Lotus','Mahindra','Maserati','Matra','Mazda',
                                'Mclaren','Mercedez Benz','Mercury','MG','MINI','Mitsubishi','Miura','Nissan','Peugeot','Plymouth','Pontiac','Porsche',
                                'RAM','RELY','Renault','Rolls-Royce','Rover','Saab','Saturn','Seat','SHINERAY','smart','SSANGYONG','Subaru','Suzuki',
                                'TAC','Toyota','Troller','Volvo','VW-VOLKSWAGEN','Wake','Walk']    
    return Response(json.dumps(marca), mimetype='application/json')

@Tabelas.route('/AutocompleteModelosDB', methods=['GET', 'POST'])
def ModelosDic():
    form= DadosEssenciais()
    marca=form.Marca.data
    res = Dado.query.order_by(marca).group_by(Dado.ModeloDB).all()
    list_modelos = [r.as_dict() for r in res]
    return jsonify(list_modelos)

@Tabelas.route('/AutocompleteMotorDB')
def MotorDic():
    res = Dado.query.group_by(Dado.VersaoDoMotorDB).all()
    list_motor = [r.as_dict() for r in res]
    return jsonify(list_motor)

@Tabelas.route('/_AutocompleteCombustivel', methods=['GET'])
def AutocompleteCombustivel():
    combustivel = ['Gasolina','Etanol','GNV','Diesel','Flex']    
    return Response(json.dumps(combustivel), mimetype='application/json')

@Tabelas.route('/_AutocompleteCor', methods=['GET'])
def AutocompleteCor():
    cor = ["Amarelo","Azul","Bege","Branco","Bronze","Cinza","Dourado","Indefinida","Laranja","Marrom","Prata","Preto","Rosa","Roxo","Verde","Vermelho","Vinho"]    
    return Response(json.dumps(cor), mimetype='application/json')

@Tabelas.route('/_AutocompleteLocal', methods=['GET'])
def AutocompleteLocal():
    local = ["Limeira", "Piracicaba"]    
    return Response(json.dumps(local), mimetype='application/json')
