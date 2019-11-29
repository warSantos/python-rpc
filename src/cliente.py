import os
import rpyc
import json
import socket
from user import User
from sys import argv, exit

# Importando módulos locais.
from base import get_opt

class Cliente():

    def criarUsuario(self):
        print("Olá.")

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
            if not data:
                print("Conexão fechada pelo servidor.")
                exit(1)
            retorno = json.loads(data)
            # Se o usuário foi autenticado.
            if retorno['aceito']:
                cmd, login, _ = texto.split()
                usuario.status = retorno['aceito']
                usuario.login = login
                usuario.dir_corrente = os.getcwd()+'/home/'+login
                break
            else:
                print(retorno['mensagem'])
        
        # Recebendo dados do CD inicial no servidor.
        data = socket_con.recv(1024)
        retorno = json.loads(data.decode())
        usuario.dir_corrente = retorno['mensagem']
        
        while True:
            prefixo = usuario.login+'@server:~'+usuario.dir_corrente+'$ '
            texto = input(prefixo)
            socket_con.send(texto.encode())
            data = socket_con.recv(1024)
            if not data:
                print("Conexão fechada pelo servidor.")
                exit(1)
            # Lendo retorno do servidor.
            retorno = json.loads(data.decode())
            print(data)
            # Interpreta o retorno do comando cd.
            if retorno['comando'] == 'cd':
                if retorno['sucesso']:
                    usuario.dir_corrente = retorno['mensagem']
                    print("NOVO DIR: ", usuario.dir_corrente)
                else:
                    print(retorno['mensagem'])
            # Interpreta o retorno do comando disconectar 
            # (vê se o server fechou também).
            elif retorno['comando'] == 'disconectar':
                print("Ola.")
                exit(0)
            # Interpreta o retorno do comando get.
            elif retorno['comando'] == 'get':
                print("Ola.")
            # Interpreta o retorno do comando ls.
            elif retorno['comando'] == 'ls':
                print(retorno['conteudo'])
            # Interpreta o retorno do comando put.
            elif retorno['comando'] == 'put':
                print("Ola.")
            # Interpreta o retorno do comando rm.
            elif retorno['comando'] == 'rm':
                print("Ola.")
            # Interpreta o retorno do comando rmdir.
            elif retorno['comando'] == 'rmdir':
                print("Ola.")
            # Trata entrada de comandos inexistentes.
            else:
                print("Ola.")
            # Atualizando o caminho no barra.
        socket_con.close()

    def conectar(self, ip_servidor_con):

        # Porta padrão de conexão do servidor de conexões TCP com socket.
        porta = 8000
        # Abrindo o socket para conexão com o servidor.
        socket_con = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # Conecatando no servidor.
        socket_con.connect((ip_servidor_con, porta))
        return socket_con

    def help(self):
        print("Ajuda.")
        print("-c: Endereço do servidor de conexões.")
        print("python3 src/conexoes.py -c IP")

if __name__=='__main__':

    # Recebendo parâmetros de entrada.
    opts = get_opt(argv[1:], "c:", help)
    clnt = Cliente()
    clnt.menu(opts['-c'])