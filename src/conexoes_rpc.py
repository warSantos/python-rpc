import re
import rpyc
import hashlib
from base import get_opt
from sys import argv, exit

class ServidorConexeosRPC(rpyc.Service):

    def help(self):
        print("Ajuda.")
        print("-c: Endereço do servidor de conexões.")
        print("-f: Endereço do servidor de arquivos.")
        print("python3 src/conexoes_rpc.py -c IP -f IP")

    # Auntentica usuário no servidor de autenticação.
    def autenticar(self, login, senha, hostname="127.0.0.1", porta=8002):
        resumo = hashlib.sha256(senha.encode()).hexdigest()
        conexao = ServidorConexeosRPC().conectar(hostname, porta)
        return conexao.root.autenticar(login, resumo)

    # Abrea conexão com um servidor RPC (arquivos ou autenticação).
    # Por padrão esta definido a porta utilizada pelo servidor de arquivos
    # em testes com uma máquina apenas.
    def conectar(self, hostname="127.0.0.1", porta=8001):
        return rpyc.connect(hostname, porta)
    
    # Navega entre os diretórios do usuário.
    def cd(self, conexao, caminho, usuario):
        return conexao.root.cd(caminho, usuario.usuario_json())

    def get(self, conn, arquivo, usuario):
        return

    # Lista os diretórios fazendo conexão com o servidor de arquivos.
    def ls(self, conexao, caminho, usuario):
        return conexao.root.ls(caminho, usuario.usuario_json())
    
    def mkdir(self, conexao, caminho, usuario):
        return conexao.root.mkdir(caminho, usuario.usuario_json())

    def rmdir(self, conexao, caminho, usuario):
        return conexao.root.rmdir(caminho, usuario.usuario_json())

    def rm(self, conexao, caminho, usuario):
        return conexao.root.rm(caminho, usuario.usuario_json())

if __name__ == "__main__":
    servidor = ServidorConexeosRPC()
    conexao = servidor.conectar("localhost", "8002")
    print(servidor.rm(conexao, "home/root/diretorio"))