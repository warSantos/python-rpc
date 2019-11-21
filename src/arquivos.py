import os
import rpyc
from sys import argv, exit

class ServidorArquivos(rpyc.Service):

    def exposed_criarHome(self, caminho):

        homedir = 'home/'+caminho
        # Se o caminho não existir
        if not os.path.exists(homedir):
            os.makedirs(homedir)
            print("Diretório criado com sucesso.")
            return ("Diretório: "+homedir+" criado com sucesso.")
        else:
            return ("O diretório: "+homedir+" já existe.")

    def exposed_teste(self):
        return "Servidor de arquivos funcionando corretamente."


if __name__=='__main__':

    hostname = argv[1]
    porta = int(argv[2])
    servidor = rpyc.ThreadPoolServer(ServidorArquivos, \
        hostname=hostname, port=porta)
    servidor.start()