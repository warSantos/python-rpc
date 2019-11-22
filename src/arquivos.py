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

    def exposed_listarDiretorio(self, caminho):

        # Se o arquivo ou diretório existir.
        if os.path.exists(caminho):
            if os.path.isdir(caminho):    
                content = os.listdir(caminho)
                content.sort()
                return '\n'.join(content)
            else:
                return caminho.split('/')[-1]
        # Se o diretório não existir.
        else:
            print("Error: diretório ou arquivo "+caminho+" não encontrado.")
            return ("Error: diretório ou arquivo "+caminho+" não encontrado.")

    def exposed_criarDiretorio(self, caminho):

        # Se o arquivo ou diretório existir.
        if os.path.exists(caminho):
            print(("Error: arquivo "+caminho+" existe."))
            return ("Error: arquivo "+caminho+" existe.")
        else:
            os.makedirs(caminho)

    def exposed_removerDiretorio(self, caminho):

        # Se o arquivo ou diretório existir.
        if not os.path.exists(caminho):
            print(("Error: arquivo "+caminho+" não encontrado."))
            return ("Error: arquivo "+caminho+" não encontrado.")
        else:
            # Se ele for um diretório, não apague e retorne erro.
            if os.path.isfile(caminho):
                print("rmdir: falhou em remover "+caminho+": Não é um arquivo")
                return ("rmdir: falhou em remover "+caminho+": Não é um arquivo")
            else:
                os.rmdir(caminho)

    def exposed_removerArquivo(self, caminho):
        # Se o arquivo ou diretório existir.
        if not os.path.exists(caminho):
            print(("Error: arquivo "+caminho+" não encontrado."))
            return ("Error: arquivo "+caminho+" não encontrado.")
        else:
            # Se ele for um arquivo, não apague e retorne erro.
            if os.path.isdir(caminho):
                print("rmdir: falhou em remover "+caminho+": Não é um diretório")
                return ("rmdir: falhou em remover "+caminho+": Não é um diretório")
            else:
                os.remove(caminho)

    def exposed_teste(self):
        return "Servidor de arquivos funcionando corretamente."


if __name__=='__main__':

    hostname = argv[1]
    porta = int(argv[2])
    servidor = rpyc.ThreadPoolServer(ServidorArquivos, \
        hostname=hostname, port=porta)
    servidor.start()