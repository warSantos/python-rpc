# import socket programming library
from sys import argv
import socket
#from _thread import *
#import threading
from multiprocessing import Pool

# Importando módulos locais.
from base import get_opt


class ServidorConexoes():

    def menu(self, conn):
        
        # Mantendo a conexão com o cliente ativa.
        while True:
            texto = str(conn[0].recv(1024))
            comandos = texto.split()
            # Menu de comandos.
            # Faz chamada de função do cd no servidor de RPC de arquivos.
            if comandos[0] == 'cd':
                print("Ola.")
            # Faz chamada de função de autenticação no servidor RPC de autenticação.
            elif comandos[0] == 'conectar':

            # Solicita desconecção com o servidor de conexões.
            elif comandos[0] == 'disconectar':
                conn[0].close()
                return
            # Faz chamada de função do get no servidor de RPC de arquivos.
            elif comandos[0] == 'get':
                print("Ola.")
            # Faz chamada de função do ls no servidor de RPC de arquivos.
            elif comandos[0] == 'ls':
                print("Olá.")
            # Faz chamada de função do put no servidor de RPC de arquivos.
            elif comandos[0] == 'put':
                print("Ola.")
            # Faz chamada de função do rm no servidor de RPC de arquivos.
            elif comandos[0] == 'rm':
                print("Ola.")
            # Faz chamada de função do rmdir no servidor de RPC de arquivos.
            elif comandos[0] == 'rmdir':
                print("Ola.")
            # Retorna erro (comando não encontrado).
            else:
                print("error: comando "+comandos[0]+" não encontrado.")
                conn[0].send("error: comando "+comandos[0]+" não encontrado.")

    def iniciarServidor(self, ip_servidor_con, ip_servidor_ftp):

        # Criando pool de processos para armazenar as conexões. Pode armazenar 20 clientes por vez.
        pool_clientes = Pool(20)

        ip_escuta = '0.0.0.0'
        porta = 8000

        # Iniciando socket de recepção de novas conexões.
        socket_conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_conexao.bind((ip_escuta, porta))
        print("Socket associado a porta", porta)

        # Permitir que o servidor escute no máximo 20 conexões por vez.
        socket_conexao.listen(20)
        print("Servidor na escuta.")

        # Lista com resultados das threads utilizadas para atender aos clientes.
        resultados = list()

        # Enquanto  servidor estiver ativo.
        while True:
            # Estabiliza a conexão com o cliente.
            socket_cliente, addr = socket_conexao.accept()
            # Inicia uma nova thread para atender o novo cliente.
            #start_new_thread(threaded, (socket_cliente,))
            res = pool_clientes.apply_async(menu, (socket_cliente, addr))
            resultados.append(res)

        # Fechando socket de escuta.
        socket_conexao.close()

        # Fechando o pool de threads e esperando as threads existentes retornarem.
        pool_clientes.close()
        pool_clientes.join()

    def help(self):
        print("Ajuda.")
        print("-c: Endereço do servidor de conexões.")
        print("-f: Endereço do servidor de arquivos.")
        print("python3 src/conexoes.py -c IP -f IP")


if __name__ == '__main__':

    opts = get_opt(argv[1:], "c:f:", help)
    servidor = ServidorConexoes()
    servidor.iniciarServidor(opts['-c'], opts['-f'])