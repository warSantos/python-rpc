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

    # Lista os diretórios fazendo conexão com o servidor de arquivos.
    def listarDiretorio(self, conexao, caminho, usuario):
        return conexao.root.listarDiretorio(caminho, usuario.usuario_json())
    
    def mkdir(self, conexao, caminho, usuario):
        return conexao.root.mkdir(caminho, usuario.usuario_json())

    def removerDiretorio(self, conexao, caminho):
        return conexao.root.removerDiretorio(caminho)

    def removerArquivo(self, conexao, caminho):
        return conexao.root.removerArquivo(caminho)

if __name__ == "__main__":
    servidor = ServidorConexeosRPC()
    conexao = servidor.conectar("localhost", "8002")
    print(servidor.removerArquivo(conexao, "home/root/diretorio"))