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
            comandos = texto.split()
            # Menu de comandos.
            if comandos[0] == 'ls':
                print("Olá.")
            elif comandos[0] == 'cd':
                print("Ola.")
            elif comandos[0] == 'get':
                print("Ola.")
            elif comandos[0] == 'put':
                print("Ola.")
            
if __name__=='__main__':
    clnt = Cliente()
    clnt.menu()