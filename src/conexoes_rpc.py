import re
import rpyc
from base import get_opt
from sys import argv, exit

class ServidorConexeosRPC(rpyc.Service):

    def help(self):
        print("Ajuda.")
        print("-c: Endereço do servidor de conexões.")
        print("-d: Porta do servidor de conexões.")
        print("-e: Endereço do servidor de arquivos.")
        print("-f: Porta do servidor de arquivos.")
        print("python3 src/conexoes_rpc.py -c IP -p d PORTA -e IP -f PORTA")

    # Abrea conexão com um servidor RPC (arquivos ou autenticação).
    def conectar(self, hostname, porta):
        return rpyc.connect(hostname, porta)
    
    # Lista os diretórios fazendo conexão com o servidor de arquivos.
    def listarDiretorio(self, conexao, caminho):
        return conexao.root.listarDiretorio(caminho)
    
    def criarDiretorio(self, conexao, caminho):
        return conexao.root.criarDiretorio(caminho)

    def removerDiretorio(self, conexao, caminho):
        return conexao.root.removerDiretorio(caminho)

    def removerArquivo(self, conexao, caminho):
        return conexao.root.removerArquivo(caminho)

if __name__ == "__main__":
    servidor = ServidorConexeosRPC()
    conexao = servidor.conectar("localhost", "8002")
    print(servidor.removerArquivo(conexao, "home/root/diretorio"))
    