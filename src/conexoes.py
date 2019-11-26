# import socket programming library
import json
import time
import socket
from sys import argv
from multiprocessing import Pool

# Importando módulos locais.
from user import User
from base import get_opt
from conexoes_rpc import ServidorConexeosRPC


def menu(conn):

    print("TODO: Iniciando servidor de escuta do cliente.", conn.getpeername())
    tentativas = 3
    # Criando objeto de servidor de conexões rpc com servidor de autenticação.
    servidor_rpc_aut = ServidorConexeosRPC()
    # Criando usário.
    usuario = User()
    # Autenticando e criando objeto usuário:
    while True:
        data = conn.recv(1024)
        if not data:
            print("Cliente desconectado.", conn.getpeername())
            conn.close()
            return
        texto = data.decode()
        comandos = texto.split()
        if comandos[0] == 'login':
            # Removendo o token de comando.
            comandos.pop(0)
            if len(comandos) != 2:
                r_json = json.dumps({"aceito": False, "mensagem": "Quantidade de parâmetros inválida."})
                conn.send(r_json.encode())
            else:
                r_json = servidor_rpc_aut.autenticar(comandos[0], comandos[1])
                resposta = json.loads(r_json)
                # Se a conexão foi realizada com sucesso.
                if resposta['aceito']:
                    # Retornando json com confirmação de autenticação.
                    conn.send(r_json.encode())
                    # Configurando o usuário.
                    usuario.login = comandos[1]
                    usuario.status = True
                    usuario.dir_corrente = 'home/'+comandos[1]
                    break
                else:
                    tentativas -= 1
                    if tentativas == 0:
                        tentativas = 3
                        resposta['mensagem'] = resposta['mensagem']+ \
                            ' Número máximo de tentativas seguidas atingido.\n'+ \
                            ' Aguarde 5 segundos e tente novamente.\n'
                        r_json = json.dumps(resposta)
                        conn.send(r_json.encode())
                        time.sleep(5)
                    else:
                        conn.send(r_json.encode())
        else:
            print("Usuário ainda não autenticado.")
            data_resposta = {}
            data_resposta['aceito'] = False
            data_resposta['mensagem'] = "Usuário ainda não autenticado."
            conn.send(json.dumps(data_resposta).encode())

    # Conectando o servidor de arquivos.
    servidor_rpc_ftp =  ServidorConexeosRPC()
    conn_rpc_ftp = servidor_rpc_ftp.conectar()
    # Menu de comandos.
    while True:
        data = conn.recv(1024)
        if not data:
            print("Cliente desconectado.", conn.getpeername())
            conn.close()
            return
        else:
            texto = data.decode()
            comandos = texto.split()
            # Faz chamada de função do cd no servidor de RPC de arquivos.
            if comandos[0] == 'cd':
                print("Ola.")
            # Solicita desconecção com o servidor de conexões.
            elif comandos[0] == 'disconectar':
                print("Cliente desconectado.", conn.getpeername())
                conn.close()
                return
            # Faz chamada de função do get no servidor de RPC de arquivos.
            elif comandos[0] == 'get':
                print("Ola.")
            # Faz chamada de função do ls no servidor de RPC de arquivos.
            elif comandos[0] == 'ls':
                # Removendo o comandos ls.
                comandos.pop(0)
                msg = ''
                for param in comandos:
                    msg += param+": \n\n"
                    msg += servidor_rpc_ftp.listarDiretorio(conn_rpc_ftp, param)+"\n"
                conn.send(msg.encode())
            elif commandos[0] == 'quit':
                print("quit.")
                conn.close()
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
                msg = "error: comando "+comandos[0]+" não encontrado."
                conn.send(msg.encode())


class ServidorConexoes():

    def iniciarServidor(self, ip_servidor_con, ip_servidor_ftp):

        # Criando pool de processos para armazenar as conexões. Pode armazenar 20 clientes por vez.
        pool_clientes = Pool(20)

        ip_escuta = '127.0.0.1'
        porta = 8000

        # Iniciando socket de recepção de novas conexões.
        socket_conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_conexao.bind((ip_escuta, porta))
        print("Socket associado a porta", porta)

        # Permitir que o servidor escute no máximo 20 conexões por vez.
        socket_conexao.listen(20)

        # Lista com resultados das threads utilizadas para atender aos clientes.
        resultados = list()

        # Enquanto  servidor estiver ativo.
        while True:
            # Estabiliza a conexão com o cliente.
            print("Servidor na escuta...")
            socket_cliente, addr = socket_conexao.accept()
            # Inicia uma nova thread para atender o novo cliente.
            res = pool_clientes.apply_async(menu, (socket_cliente,))
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
