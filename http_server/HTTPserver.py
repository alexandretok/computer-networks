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
	print "\n" + request

	try:
		# Separa o request por linha e guarda a primeira
		arquivo = request.split('\n')[0]

		# Separa a primeira linha por espacos e pega o primeiro item
		metodo = arquivo.split()[0]

		# Separa a primeira linha por espacos e pega o segundo item
		arquivo = arquivo.split()[1]
	except:
		http_response = """\
HTTP/1.1 500 Internal Server Error \r\n\r\n
<html><head></head><body><h2>Erro 500</h2><h3>Ops, um erro desconhecido ocorreu.</h3><a href="javascript:history.back();">Voltar</a></body></html>\r\n
"""
		# servidor retorna o que foi solicitado pelo cliente (neste caso a resposta e generica)
		client_connection.send(http_response)
		# encerra a conexao
		client_connection.close()
		continue


	# Remove a barra do inicio do arquivo
	arquivo = arquivo[1:]

	if arquivo == "":
		arquivo = 'index.html'
	
	print "\nMetodo: " + metodo
	print "Arquivo solicitado: " + arquivo

	if metodo != 'GET':
		# Se o metodo utilizado nao foi o GET, envia erro 400
		http_response = """\
HTTP/1.1 400 Bad Request \r\n\r\n
<html><head></head><body><h2>Erro 400</h2><h3>Sua requisicao e invalida. Utilize o metodo GET</h3><a href="javascript:history.back();">Voltar</a></body></html>\r\n
"""
		print "400 Bad Request"
	else:
		if os.path.isfile(arquivo):
			file = open(arquivo, 'r')

			# declaracao da resposta do servidor
			http_response = """\
HTTP/1.1 200 OK \r\n\r\n
"""
			# Adiciona o conteudo do arquivo a resposta do servidor
			http_response += file.read()

			print "200 OK"

			# Fecha o arquivo
			file.close()
		else:
			# Se o arquivo nao existir, envia erro 404
			http_response = """
			HTTP/1.1 404 Not Found\r\n\r\n
<html><head></head><body><h2>Erro 404</h2><h3>Que pena, o arquivo solicitado nao foi encontrado.<br>Tente novamente proximo semestre.</h3><a href="javascript:history.back();">Voltar</a></body></html>\r\n
"""
			print "404 Not Found"
	
	# servidor retorna o que foi solicitado pelo cliente (neste caso a resposta e generica)
	client_connection.send(http_response)
	# encerra a conexao
	client_connection.close()

# encerra o socket do servidor
listen_socket.close()