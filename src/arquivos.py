import io
import os
import json
import rpyc
from user import User
from sys import argv, exit

# Importando módulos locais.
from base import permissao_acesso


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

    def exposed_cd(self, caminho, json_usuario):

        usuario = User().json_loads(json_usuario)
        # Atualizando o diretório do processo com o do cliente.
        data = {}
        # Se o arquivo existir e for um diretório.
        print("Antes destino:", caminho, "Antes SO:", os.getcwd())
        os.chdir(usuario.dir_corrente)
        if os.path.exists(caminho):
            if os.path.isdir(caminho):
                # Se o usuário poder acessar esse diretório
                if permissao_acesso(caminho, usuario):
                    data['sucesso'] = True
                    os.chdir(caminho)
                    data['mensagem'] = os.getcwd()
                    # Sicronizando o diretório com o usuário.
                    print("Depois: ", caminho, os.getcwd(), '\n\n')
                # Se o usuário não tiver permissão.
                else:
                    data['sucesso'] = False
                    data['mensagem'] = "error: permissão negada.\n"
                return json.dumps(data)
            else:
                data['sucesso'] = False
                data['mensagem'] = "bash: cd: "+caminho+": Não é um diretório"
                return json.dumps(data)
        else:
            data['sucesso'] = False
            data['mensagem'] = "bash: cd: "+caminho + \
                ": Arquivo ou diretório inexistente"
            return json.dumps(data)

    #def exposed_get(self, arquivo, json_usuario):
    def exposed_get(self, caminho, json_usuario):
        
        usuario = User().json_loads(json_usuario)
        # Atualizando o diretório do processo com o do cliente.
        data = {}
        data['sucesso'] = True
        os.chdir(usuario.dir_corrente)
        pt = io.open(caminho,'rb', \
            buffering=1024, encoding=None, errors=None, \
                newline=None, closefd=True)
        data['conteudo'] = pt.read()
        return data

    def exposed_ls(self, caminho, json_usuario):

        usuario = User().json_loads(json_usuario)
        # Sincronizando o diretório do processo com o do usuário.
        os.chdir(usuario.dir_corrente)
        # Se o arquivo ou diretório existir.
        if os.path.exists(caminho):
            # Se for um diretório.
            if os.path.isdir(caminho):
                # Se o usuário tiver permissão para acessar o diretório.
                if permissao_acesso(caminho, usuario):
                    content = os.listdir(caminho)
                    content.sort()
                    return '\n'.join(content)
                else:
                    return 'ls: não foi possível abrir o diretório' + \
                        caminho+': Permissão negada'
            # Se for um arquivo.
            else:
                tokens = caminho.split('/')
                tokens.pop()
                dir_dest = '/'.join(tokens)
                # Se o usuário tiver permissão para acessar o diretório onde esta o arquivo.
                if permissao_acesso(dir_dest, usuario):
                    return caminho.split('/')[-1]
                else:
                    return 'ls: não foi possível abrir o diretório' + \
                        caminho+': Permissão negada'
        # Se o diretório não existir.
        else:
            print("Error: diretório ou arquivo "+caminho+" não encontrado.")
            return ("Error: diretório ou arquivo "+caminho+" não encontrado.")

    def exposed_mkdir(self, caminho, json_usuario):

        usuario = User().json_loads(json_usuario)
        # Sincronizando o diretório do processo com o do usuário.
        os.chdir(usuario.dir_corrente)
        # Se o caminho for absoluto.
        if caminho[0] == '/':
            # Verificando se o usuário ter permissão no caminho
            tokens = caminho.split('/')
            # Removendo possíveis ''
            if len(tokens[-1]) == 0:
                tokens.pop()
            while len(tokens) > 0:
                c = '/'+'/'.join(tokens)
                # Se o caminho existir.
                if os.path.exists(c):
                    # Se o usuário tiver permissão.
                    if permissao_acesso(c, usuario):
                        # Se o caminho todo existir.
                        if os.path.exists(caminho):
                            return ("mkdir: não foi possível criar o diretório"+c +
                                    "Arquivo existe")
                        else:
                            os.makedirs(caminho)
                        return (caminho+": criado com sucesso.")
                    else:
                        return ("mkdir: não foi possível criar o diretório " +
                                caminho+" Permissão negada")
                tokens.pop()
        # Se o caminho for relativo.
        else:
            tokens = caminho.split('/')
            # Removendo possívels ''
            if len(tokens[-1]) == 0:
                tokens.pop()
            for t in tokens:
                # Se o diretório p existir.
                if os.path.exists(t):
                    # Entre e veja se o usuário tem permissão.
                    if permissao_acesso(t, usuario):
                        os.chdir(t)
                    # Se em algum momento o usuário não tiver permissão.
                    else:
                        return ("mkdir: não foi possível criar o diretório " +
                                caminho+" Permissão negada")
                else:
                    os.makedirs(caminho)
                    return (caminho+": criado com sucesso.")
            # Se ele percorreu todos os diretórios e todos existiam.
            return ("mkdir: não foi possível criar o diretório"+caminho +
                    "Arquivo existe")

    def exposed_rmdir(self, caminho, json_usuario):

        usuario = User().json_loads(json_usuario)
        # Sincronizando o diretório do processo com o do usuário.
        os.chdir(usuario.dir_corrente)
        # Se o caminho for absoluto.
        if caminho[0] == '/':
            # Verificando se o usuário ter permissão no caminho
            tokens = caminho.split('/')
            # Removendo possíveis ''
            if len(tokens[-1]) == 0:
                tokens.pop()
            # Removendo caracter nulo.
            _ = tokens.pop(0)
            final = tokens.pop()
            while len(tokens) > 0:
                c = '/'+'/'.join(tokens)
                # Se o caminho existir.
                if os.path.exists(c):
                    # Se o usuário tiver permissão.
                    if permissao_acesso(c, usuario):
                        os.chdir(c)
                        break
                    else:
                        return ("rmdir: não foi possível remover o diretório " +
                                caminho+" Permissão negada.")
                tokens.pop()
            # Se o caminho todo existir.
            if os.path.exists(caminho):
                if os.path.isdir(caminho):
                    if len(os.listdir(caminho)) == 0:
                        os.rmdir(caminho)
                        return ("rmdir: diretório"+caminho+"removido.")
                    else:
                        return("rmdir: falhou em remover"+caminho \
                        +" Diretório não vazio.")
                else:
                    return ("rmdir: não foi possível remover"+caminho \
                        +": Não é um diretório.")
            else:
                return ("rmdir: não foi possível remover o diretório"+c +
                        "Arquivo não encontrado.")
        # Se o caminho for relativo.
        else:
            tokens = caminho.split('/')
            # Removendo possívels ''
            if len(tokens[-1]) == 0:
                tokens.pop()
            # Removendo o nome do arquivo para poder navegar por diretórios.
            final = tokens.pop()
            for t in tokens:
                # Se o diretório p existir.
                if os.path.exists(t):
                    # Entre e veja se o usuário tem permissão.
                    if permissao_acesso(t, usuario):
                        os.chdir(t)
                    else:
                        return ("rmdir: não foi possível remover o diretório " +
                            caminho+" Permissão negada")
            # Se o caminho todo existir.
            if os.path.exists(final):
                if os.path.isdir(final):
                    if len(os.listdir(final)) == 0:
                        # Colocando o processo no diretório corrente do usuário.
                        os.rmdir(final)
                        return ("rmdir: diretório"+caminho+"removido.")
                    else:
                        return("rmdir: falhou em remover"+caminho \
                        +" Diretório não vazio.")
                else:
                    return ("rmdir: não foi possível remover"+caminho \
                        +": Não é um diretório.")
            else:
                return ("rmdir: não foi possível remover o diretório"+caminho+
                        "Arquivo não encontrado.")

    def exposed_rm(self, caminho):
        # Se o arquivo ou diretório existir.
        if not os.path.exists(caminho):
            print(("Error: arquivo "+caminho+" não encontrado."))
            return ("Error: arquivo "+caminho+" não encontrado.")
        else:
            # Se ele for um arquivo, não apague e retorne erro.
            if os.path.isdir(caminho):
                print("rmdir: falhou em remover " +
                      caminho+": Não é um diretório")
                return ("rmdir: falhou em remover "+caminho+": Não é um diretório")
            else:
                os.remove(caminho)

    def exposed_teste(self):
        print(dir(self))
        return "Servidor de arquivos funcionando corretamente."


if __name__ == '__main__':

    hostname = argv[1]
    porta = int(argv[2])
    servidor = rpyc.ForkingServer(ServidorArquivos,
                                  hostname=hostname, port=porta)
    servidor.start()
