# LINKS
# ROUTES

from flask import render_template, redirect, url_for, flash, request
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil
from comunidadeimpressionadora.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image

lista_usuarios = ['Lira', 'João', 'Alon', 'Alessandra', 'Amanda']

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/usuarios')
@login_required
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')  # par_next (leia-se parâmetro next, que é a pagina que o usuário queria acessar antes do login)
            if par_next:
                return  redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no Login. E-mail ou Senha incorretos', 'alert-danger')
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        # Criptografia de senha
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        # Criar o usuário
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        # Adicionar a sessão
        database.session.add(usuario)
        # commit na sessão
        database.session.commit()
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com sucesso', 'alert-success')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar')
@login_required
def criar_post():
    return render_template('criarpost.html')

def salvar_imagem(imagem):
    # adicionar um código aleatório no nome da imagem
    codigo = secrets.token_hex(8) #gera um código de 8 bytes
    # separar o nome do arquivo da extensão dele
    nome, extensao = os.path.splitext(imagem.filename)
    #agora juntando o nome+código+extensão
    #nome_completo = os.path.join(nome, codigo, extensao)
    nome_arquivo = nome + codigo + extensao
    #agora preciso estabelecer o caminho de onde a imagem se encontra
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    # reduzir o tamanho da imagem. Será uma tupla (tamanho x altura)
    tamanho = (200,200) #Primeiro definir essa tupla. São as dimensões da imagem definidas lá no nosso perfil.html
    #reduzindo efetivamente. Mas...
    #Temos que instalar o 'Pillow' (pip install Pillow). É uma biblioteca para compactar imagem
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    # salvar a imagem na pasta fotos_perfil
    imagem_reduzida.save(caminho_completo)
    # mudar o campo foto_perfil do usuário para o novo nome da imagem
    return nome_arquivo

def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
       if 'curso_' in campo.name:
           if campo.data:
           #adicionar o texto do campo.label (Excel Impressionador) na lista de cursos
            lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            #adicionar um código aleatório no nome da imagem
            #reduzir o tamanho da imagem
            #salvar a imagem na pasta fotos_perfil
            #mudar o campo foto_perfil do usuário para o novo nome da imagem
            #MAS TODOS ESSES PASSOS ACIMA SE RESUMEM NO FUNÇÃO DA LINHA 76
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash(f'Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET": #vai preencher automaticamente os campos Nome usuário e e-mail, na página editar perfil
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)