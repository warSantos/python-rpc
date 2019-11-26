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
            texto = input(usuario.dir_corrente)
            socket_con.send(texto.encode())
            data = socket_con.recv(1024)
            if not data:
                print("Conexão fechada pelo servidor.")
                exit(1)
            resposta = json.loads(data)
            # Se o usuário foi autenticado.
            if resposta['aceito']:
                cmd, login, _ = texto.split()
                usuario.status = resposta['aceito']
                usuario.login = login
                usuario.dir_corrente = 'home/'+login
                break
            else:
                print(resposta['mensagem'])
        
        while True:
            prefixo = usuario.login+'@server:~/'+usuario.dir_corrente+'$ '
            texto = input(prefixo)
            socket_con.send(texto.encode())
            data = socket_con.recv(1024)
            if not data:
                print("Conexão fechada pelo servidor.")
                exit(1)
            print(data.decode())
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