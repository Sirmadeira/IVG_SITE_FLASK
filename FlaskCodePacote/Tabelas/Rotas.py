from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint)
from flask_login import current_user, login_required
from sqlalchemy import func, desc
from FlaskCodePacote import db
from FlaskCodePacote.Modelos import Dado
from FlaskCodePacote.Tabelas.Formularios import DadosEssenciais


Tabelas = Blueprint('Tabelas', __name__)   


@Tabelas.route("/SegundaJanela", methods=['GET', 'POST'])
@login_required
def SegundaJanela():
    form = DadosEssenciais(request.form)
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
        return redirect(url_for('Tabelas.TerceiraJanela'))
    except:
        return 'Ouve um problema deletando essa linha!'