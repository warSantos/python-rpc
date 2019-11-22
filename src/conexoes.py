# import socket programming library 
from sys import argv
import socket
from base import get_opt
from _thread import *
import threading

# Importando módulos locais.

class ServidorConexoes():

    def servidor(self):
        print("Olá.")
    
    def help(self):
        print("Ajuda.")
        print("-c: Endereço do servidor de conexões.")
        print("-d: Porta do servidor de conexões.")
        print("-e: Endereço do servidor de arquivos.")
        print("-f: Porta do servidor de arquivos.")
        print("python3 src/conexoes.py -c IP -p d PORTA -e IP -f PORTA")

if __name__=='__main__':
    
    opts = get_opt(argv[1:], "c:d:e:f:", help)
    print(opts)