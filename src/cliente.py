import rpyc
from sys import argv, exit

class Cliente():

    def criarUsuario(self):
        print("Olá.")

    def conectar(self):
        print("Ola.")
    
    def menu(self):
        diretorio = '$ '
        while True:
            texto = input(diretorio)
            print(texto)
            
if __name__=='__main__':
    clnt = Cliente()
    clnt.menu()