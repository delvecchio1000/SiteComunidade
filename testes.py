# ESTE ARQUIVO TEM O OBJETIVO EXCLUSIVO DE ENSINAR OS PRINCIPAIS COMANDOS E TÉCNICAS
# USADAS PARA CRIAÇÃO E UTILIZAÇÃO DO BANCO DE DADOS. ESTE ARQUIVO PODE SER DELETADO.
# PREFIRO MANTER COMO FONTE DE CONSULTA.

from main import app
from comunidadeimpressionadora.models import Usuario, Post
from comunidadeimpressionadora import database

# Observação: Toda vez que modificarmos ou consultarmos o banco de dados
# será preciso inserir os comandos dentro de um 'with app.app_context():'

#with app.app_context(): # Linhas comentadas pois só precisa ser executado uma vez para criação do banco de dados
#   database.create_all()

#with app.app_context(): # Linhas comentadas pois só precisa ser executado uma vez para criação dos usuários
#   usuario = Usuario(username="Lira", email="lira@gmail.com", senha="123456")
#   usuario2 = Usuario(username="João", email="joao@gmail.com", senha="123456")
#   database.session.add(usuario)
#   database.session.add(usuario2)
#   database.session.commit()

# Como pegar informações do banco de dados. Realizando consultas

with app.app_context():
   meus_usuarios = Usuario.query.all()

#   primeiro_usuario = Usuario.query.first()
#   print(primeiro_usuario)
   # OU
#   primeiro_usuario = meus_usuarios[0]
   segundo_usuario = meus_usuarios[1]
   print(segundo_usuario)

   # pegando informações do usuário
#   print(primeiro_usuario.id)
#   print(primeiro_usuario.email)
   print(segundo_usuario.senha)
#   print(primeiro_usuario.username)
#   print(primeiro_usuario.posts) # Se não tiver post ainda, uma lista vazia será exibida

   # consultando um usuário baseado em uma condição
#   usuario_teste = Usuario.query.filter_by(id=2).first() # só quero pegar o primeiro usuário dessa consulta
#   print(usuario_teste)
#   print(usuario_teste.email) # quero exibir o email do usuário que tenha o id=2

   # no '.filter_by(id=2)', podemos pegar outras informações (que estejam nas classes do arquivo models.py)
#   usuario_teste = Usuario.query.filter_by(email='lira@gmail.com').first()  # só quero pegar o primeiro usuário dessa consulta
#   print(usuario_teste)
#   print(usuario_teste.email)  # quero exibir o email do usuário que tenha o id=2

   # Note que nossa tabela de usuário, da classe Usuario do arquivo models.py, está relacionada com a tabela de posts, da classe Post,
   # também do arquivo models.py . Dessa maneira posso descobrir qual é o email do usuário de um determinado post

# Linhas comentadas pois só precisa ser executado uma vez para criação do post
#   meu_post = Post(id_usuario=1, titulo="Primeiro Post do Lira", corpo="Lira voando")
#   database.session.add(meu_post)
#   database.session.commit()

#   post = Post.query.all()
#   print(post) # Vai exibir todos os posts, que no caso é uma lista que só tem um único post por enquanto ( [<Post 1>] )

   # quero pegar o primeiro post, e desse post, algumas outras informações
#   post = Post.query.first()
#   print(post.titulo)
#   print(post.id)
#   print(post.corpo)
#   print(post.autor) # Lembra da Classe Usuario que contém um parâmetro 'backref='autor', lá no arquivo models.py?
#   print(post.autor.email)

# ESTE ARQUIVO TEM O OBJETIVO EXCLUSIVO DE ENSINAR OS PRINCIPAIS COMANDOS E TÉCNICAS
# USADAS PARA CRIAÇÃO E UTILIZAÇÃO DO BANCO DE DADOS. ESTE ARQUIVO PODE SER DELETADO.
# PREFIRO MANTER COMO FONTE DE CONSULTA.

#   database.drop_all() # Deletando o banco de dados e portanto, destruindo todas as informações que colocamos durante essa aula.
#   database.create_all() # Recriando o banco de dados. Desta vez ele estará sem nenhum registro.
