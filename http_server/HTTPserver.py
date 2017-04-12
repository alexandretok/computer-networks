# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: PROF. CARLOS M D VIEGAS (viegas 'at' dca.ufrn.br)
#
# SCRIPT: Base de um servidor HTTP
#

# importacao das bibliotecas
import socket
import os.path

# definicao do host e da porta do servidor
HOST = '' # ip do servidor (em branco)
PORT = 8080 # porta do servidor

# cria o socket com IPv4 (AF_INET) usando TCP (SOCK_STREAM)
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# permite que seja possivel reusar o endereco e porta do servidor caso seja encerrado incorretamente
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# vincula o socket com a porta (faz o "bind" do IP do servidor com a porta)
listen_socket.bind((HOST, PORT))

# "escuta" pedidos na porta do socket do servidor
listen_socket.listen(1)

# imprime que o servidor esta pronto para receber conexoes
print 'Servidor HTTP aguardando conexoes na porta %s ...' % PORT

while True:
	# aguarda por novas conexoes
	client_connection, client_address = listen_socket.accept()
	# o metodo .recv recebe os dados enviados por um cliente atraves do socket
	request = client_connection.recv(1024)
	# imprime na tela o que o cliente enviou ao servidor
	# print request

	# Separa o request por linha, a primeira linha pelos espacos e depois remove o primeiro caractere (a barra) do segundo elemento
	print request.split('\n')[0]
	arquivo = request.split('\n')[0].split()[1][1:]
	metodo = request.split('\n')[0].split()[0]
	print metodo
	print "Arquivo solicitado: " + arquivo

	if metodo != 'GET':
		http_response = """\
		HTTP/1.1 400 Bad Request \r\n\r\n
		<html><head></head><body><h2>Sua requisicao e invalida. Utilize o metodo GET</h2><a href="javascript:history.back();">Voltar</a></body></html>\r\n
		"""
	else:

		if arquivo == "":
			arquivo = 'index.html'
		if os.path.isfile(arquivo):
			file = open(arquivo, 'r')
			# declaracao da resposta do servidor
			http_response = """\
	HTTP/1.1 200 OK

	"""
			http_response += file.read()
			file.close()
		else:
			http_response = """
			HTTP/1.1 404 Not Found\r\n\r\n
	<html><head></head><body><h3>Que pena, o arquivo solicitado nao foi encontrado.<br>Tente novamente proximo semestre.</h3></body></html>\r\n
	"""
	
	# servidor retorna o que foi solicitado pelo cliente (neste caso a resposta e generica)
	client_connection.send(http_response)
	# encerra a conexao
	client_connection.close()

# encerra o socket do servidor
listen_socket.close()