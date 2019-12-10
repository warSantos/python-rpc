import os
import ssl
import rpyc
import json
import socket
from user import User
from sys import argv, exit

# Importando módulos locais.
from base import get_opt


class Cliente():

    def menu(self, ip_servidor_con):

        # Abrindo conexão com o servidor.
        socket_con = Cliente().conectar(ip_servidor_con)
        # Criando um usuário para conexão.
        usuario = User()
        # Enquanto o usuário não se auntenticar.
        while True:
            #texto = input(usuario.dir_corrente)
            texto = "login welton 123"
            socket_con.send(texto.encode())
            data = socket_con.recv(1024)
            print(data)
            if not data:
                print("Conexão fechada pelo servidor.")
                exit(1)
                socket_con.close()
            retorno = json.loads(data)
            # Se o usuário foi autenticado.
            if retorno['aceito']:
                cmd, login, _ = texto.split()
                usuario.status = retorno['aceito']
                usuario.login = login
                usuario.dir_corrente = retorno['user_home']
                break
            else:
                print(retorno['conteudo'])

        # Recebendo dados do CD inicial no servidor.
        data = socket_con.recv(1024)
        retorno = json.loads(data.decode())
        usuario.dir_corrente = retorno['conteudo']

        while True:
            prefixo = usuario.login+'@server:~'+usuario.dir_corrente+'$ '
            texto = input(prefixo)
            socket_con.send(texto.encode())
            data = socket_con.recv(1024)
            if not data:
                print("Conexão fechada pelo servidor.")
                exit(1)
                socket_con.close()
            # Lendo retorno do servidor.
            print(data)
            retorno = json.loads(data.decode())
            # Interpreta o retorno do comando cd.
            if retorno['comando'] == 'cd':
                if retorno['sucesso']:
                    usuario.dir_corrente = retorno['conteudo']
                else:
                    print(retorno['conteudo'])
            # Interpreta o retorno do comando disconectar
            # (vê se o server fechou também).
            elif retorno['comando'] == 'disconectar':
                print("Ola.")
                exit(0)
            # Interpreta o retorno do comando get.
            elif retorno['comando'] == 'get':
                # Se o arquivo existe e pode ser baixado.
                if retorno['sucesso']:
                    nome = retorno['conteudo'].split('/')[-1]
                    pt = open(nome, 'wb')
                    while True:
                        texto = socket_con.recv(1024)
                        if len(texto) < 1024:
                            pt.write(texto.replace(b'\x00', b''))
                            break
                        pt.write(texto)
                    pt.close()
                else:
                    print(retorno['conteudo'])
            # Interpreta o retorno do comando ls.
            elif retorno['comando'] == 'ls':
                print(retorno['conteudo'])
            elif retorno['comando'] == 'mkdir':
                print(retorno['conteudo'])
            elif retorno['comando'] == 'quit':
                socket_con.shutdown(socket.SHUT_RDWR)
                exit(0)
            # Interpreta o retorno do comando put.
            elif retorno['comando'] == 'put':
                if retorno['sucesso']:
                    # Se o arquivo a ser transferido não existe.
                    if not os.path.exists(retorno['origem']) or \
                        os.path.isdir(retorno['origem']):
                        retorno['confirmado'] = False
                        socket_con.send(json.dumps(retorno).encode())
                        print("put: error: Arquivo não existe ou é um diretório.")
                    else:
                        retorno['confirmado'] = True
                        socket_con.send(json.dumps(retorno).encode())
                        pt = open(retorno['origem'], 'rb')
                        texto = ''
                        while True:
                            t = pt.read(1024)
                            # Se acabar o conteúdo do arquivo pare de enviar.
                            if len(t) < 1024:
                                socket_con.send(t+'\0'.encode())
                                break
                            socket_con.send(t)
                        pt.close()
                else:
                    print(retorno['conteudo'])
            # Interpreta o retorno do comando rm.
            elif retorno['comando'] == 'rm':
                print("Ola.")
            # Interpreta o retorno do comando rmdir.
            elif retorno['comando'] == 'rmdir':
                print(retorno['conteudo'])
            elif retorno['comando'] == 'useradd':
                print(retorno['conteudo'])
            # Trata entrada de comandos inexistentes.
            else:
                print(retorno['conteudo'])
            # Atualizando o caminho no barra.
        socket_con.close()

    def conectar(self, ip_servidor_con):

        # Porta padrão de conexão do servidor de conexões TCP com socket.
        porta = 8000
        # Criando contexto ssl para tunelamento do socket.
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip_servidor_con, porta))
        socket_con = context.wrap_socket(sock, server_hostname=ip_servidor_con)
        return socket_con

    def ajuda(self):
        print("Ajuda.")
        print("-c: Endereço IP do servidor de conexões.")
        print("python3 src/conexoes.py -c IP")


if __name__ == '__main__':

    # Recebendo parâmetros de entrada.
    clnt = Cliente()
    opts = get_opt(argv[1:], "c:", clnt.ajuda)
    clnt.menu(opts['-c'])
