import rpyc
from sys import argv, exit

class ServidorAutenticacao(rpyc.Service):

    def autenticar(self):
        print("Autenticado.")

    def exposed_teste(self):
        return "Servidor de autenticação funcionando corretamente."

if __name__=='__main__':

    hostname = argv[1]
    porta = int(argv[2])
    servidor = rpyc.ThreadPoolServer(ServidorAutenticacao, \
        hostname=hostname, port=porta)
    servidor.start()
