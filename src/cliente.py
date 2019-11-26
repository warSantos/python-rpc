import rpyc
import socket
from sys import argv, exit

# Importando módulos locais.
from base import get_opt

class Cliente():

    def criarUsuario(self):
        print("Olá.")

    def menu(self, ip_servidor_con):
        
        # Abrindo conexão com o servidor.
        socket_con = Cliente().conectar(ip_servidor_con)
        diretorio = '$ '
        while True:
            texto = input(diretorio)
            socket_con.send(texto.encode())
            data = socket_con.recv(1024)
            if not data:
                print("Conexão fechada pelo servidor.")
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