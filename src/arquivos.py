import rpyc
from sys import argv, exit

class ServidorArquivos(rpyc.Service):

    def exposed_teste(self):
        return "Servidor de arquivos funcionando corretamente."


if __name__=='__main__':

    hostname = argv[1]
    porta = int(argv[2])
    servidor = rpyc.ThreadPoolServer(ServidorArquivos, \
        hostname=hostname, port=porta)
    servidor.start()