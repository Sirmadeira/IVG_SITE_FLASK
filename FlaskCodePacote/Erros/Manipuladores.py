from flask import Blueprint, render_template

Erros = Blueprint('Erros', __name__)


@Erros.app_errorhandler(404)
def erro_404(erro):
	return render_template('Erros/404.html'), 404

@Erros.app_errorhandler(403)
def erro_403(erro):
	return render_template('Erros/403.html'), 403

@Erros.app_errorhandler(500)
def erro_500(erro):
	return render_template('Erros/500.html'), 500
