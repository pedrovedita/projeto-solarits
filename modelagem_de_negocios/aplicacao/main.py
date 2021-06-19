from flask import Flask, render_template, session, flash, url_for, redirect
from modelagem_de_negocios.persistencia.codigo import cadastro, login
from modelagem_de_negocios.util import pathing
from modelagem_de_negocios.aplicacao import algoritmo

'''
set FLASK_DEBUG=1
set FLASK_ENV=development
set FLASK_APP=modelagem_de_negocios.aplicacao.main.py
flask run
'''

rota = pathing.Path()
app = Flask(__name__, template_folder=rota.templateWay(), static_folder=rota.staticWay())
app.secret_key = 'ventodonorte'

@app.route('/')
def index():
    return render_template('index.html')

#---FUNCIONALIDADES---
@app.route('/quemsomos')
def quemSomos():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Voce deve estar logado para acessar esta função')
        return redirect(url_for('formLogin'))
    return render_template('quemsomos.html')

#---PROPOSTA---
@app.route('/proposta')
def proposta():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Voce deve estar logado para acessar esta função')
        return redirect(url_for('formLogin'))
    return render_template('algoritmo.html')

@app.route('/geraproposta', methods=['POST'])
def geraProposta():
    proposta = algoritmo.Proposta()
    res = proposta.calculo(session['cep'])
    return render_template('proposta.html', rep=res)

#---CADASTRO---
@app.route('/cadastro')
def formCadastro():
    return render_template('cadastro.html')

@app.route('/cadastracliente', methods=['POST'])
def cadastraCliente():
    cad_c = cadastro.ContaCliente()
    cad_c.cadastra()
    flash('Cliente cadastrado com sucesso!')

    return redirect(url_for('formLogin'))

@app.route('/cadastraempresa', methods=['POST'])
def cadastraEmpresa():
    cad_e = cadastro.ContaEmpresa()
    cad_e.cadastra()
    flash('Empresa cadastrada com sucesso!')

    return redirect(url_for('formLogin'))

#---LOGIN---
@app.route('/login')
def formLogin():
    return render_template('login.html')

@app.route('/logincliente', methods=['POST'])
def loginCliente():
    log_c = login.LoginCliente()

    if log_c.loga():
        session['usuario_logado'] = log_c.getDados('user')

        session['cep'] = int(log_c.getDados('cep'))
        flash(f"Olá, {session['usuario_logado']}! Login efetuado com sucesso!")
        return redirect(url_for('index'))

    flash('Usuário ou senha incorretos, tente novamente')
    return redirect(url_for('formLogin'))

@app.route('/loginempresa', methods=['POST'])
def loginEmpresa():
    log_e = login.LoginEmpresa()

    if log_e.loga():
        session['usuario_logado'] = log_e.getDados('user')
        flash(f"Olá, {session['usuario_logado']}! Login efetuado com sucesso!")
        return redirect(url_for('index'))

    flash(f'Usuário ou senha incorretos, tente novamente')
    return redirect(url_for('formLogin'))

#---LOGOUT---
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    session['cep'] = None
    flash('Usuário deslogado, faça o login novamente para ter acesso a todas funcionalidades do site')

    return redirect(url_for('index'))

app.run()