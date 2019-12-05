import io
import os
import ssl
import json
import rpyc
from user import User
from sys import argv, exit

# Importando módulos locais.
from base import permissao_acesso


class ServidorArquivos(rpyc.classic.ClassicService):

    def criarHome(self, caminho):

        homedir = 'home/'+caminho
        # Se o caminho não existir
        if not os.path.exists(homedir):
            os.makedirs(homedir)
            print("Diretório criado com sucesso.")
            return ("Diretório: "+homedir+" criado com sucesso.")
        else:
            return ("O diretório: "+homedir+" já existe.")

    def cd(self, caminho, json_usuario):

        usuario = User().json_loads(json_usuario)
        # Atualizando o diretório do processo com o do cliente.
        data = {}
        # Se o arquivo existir e for um diretório.
        os.chdir(usuario.dir_corrente)
        if os.path.exists(caminho):
            if os.path.isdir(caminho):
                # Se o usuário poder acessar esse diretório
                if permissao_acesso(caminho, usuario):
                    data['sucesso'] = True
                    # Sicronizando o diretório com o usuário.
                    os.chdir(caminho)
                    data['mensagem'] = os.getcwd()
                # Se o usuário não tiver permissão.
                else:
                    data['sucesso'] = False
                    data['mensagem'] = "error: permissão negada.\n"
            else:
                data['sucesso'] = False
                data['mensagem'] = "bash: cd: "+caminho+": Não é um diretório"
        else:
            data['sucesso'] = False
            data['mensagem'] = "bash: cd: "+caminho + \
                ": Arquivo ou diretório inexistente"
        return json.dumps(data)

    def get(self, caminho, json_usuario):

        usuario = User().json_loads(json_usuario)
        # Atualizando o diretório do processo com o do cliente.
        os.chdir(usuario.dir_corrente)
        data = {}
        tokens = caminho.split('/')
        final = tokens.pop()
        c = '/'.join(tokens)
        # Verificando se o arquivo existe.
        if os.path.exists(caminho):
            if not os.path.isdir(caminho):
                # Verificando se o usuário tem permissão para acessar o arquivo.
                if permissao_acesso(c, usuario):
                    data['sucesso'] = True
                    dir_bkp = os.getcwd()
                    if c != '':
                        os.chdir(c)
                    data['conteudo'] = '/'.join([os.getcwd(), final])
                    os.chdir(dir_bkp)
                else:
                    data['sucesso'] = False
                    data['conteudo'] = "get: não foi possível obter estado de " +\
                    caminho+": Permissão negada"
            else:
                data['sucesso'] = False
                data['conteudo'] = "get: não foi possível obter estado de " +\
                caminho+": É um diretório"
        else:
            data['sucesso'] = False
            data['conteudo'] = "get: não foi possível obter estado de " +\
                caminho+" Arquivo ou diretório inexistente"
        return json.dumps(data)

    def ls(self, caminho, json_usuario):

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

    def mkdir(self, caminho, json_usuario):

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

    def put(self, caminhos, json_usuario):

        origem = caminhos[0]
        destino = caminhos[1]
        usuario = User().json_loads(json_usuario)
        # Atualizando o diretório do processo com o do cliente.
        os.chdir(usuario.dir_corrente)
        data = {}
        data['origem'] = origem
        # Se o caminho for absoluto.
        if destino == '/':
            tokens = destino.split('/')
            # Removendo possíveis ''
            if len(tokens[-1]) == 0:
                tokens.pop()
            while len(tokens) > 0:
                c = '/'+'/'.join(tokens)
                if os.path.exists(c) and os.path.isdir(c):
                    # Se o usuário tiver permissão.
                    if permissao_acesso(c, usuario):
                        if os.path.exists(destino):
                            data['sucesso'] = True
                            # Se o usuário esta tentando por o arquivo em um dir..
                            if os.path.isdir(destino):
                                data['conteudo'] = destino + \
                                    '/'+origem.split('/')[-1]
                            # Se o usuário esta tentando substituir ou criar um arquivo
                            # no servidor de arquivos.
                            else:
                                data['conteudo'] = destino
                        else:
                            dst = destino.split('/')
                            dst.pop()
                            # Se o arquivo não existir mas o diretório anterior sim
                            # então crie um novo arquivo neste diretório.
                            if os.path.exists('/'+'/'.join(dst)):
                                data['sucesso'] = True
                                data['conteudo'] = destino
                            # Se o arquivo não existe o diretório também.
                            else:
                                data['sucesso'] = False
                                data['conteudo'] = "put: não foi possível criar arquivo comum"+destino +\
                                    ": Arquivo ou diretório inexistente."
                    else:
                        data['sucesso'] = False
                        data['conteudo'] = "put: não foi possível criar o diretório " +\
                                destino+" Permissão negada")
                tokens.pop()
        # Se o destinor relativo.
        else:
            tokens=destino.split('/')
            # Removendo possíveis ''
            if len(tokens[-1]) == 0:
                tokens.pop()
            for t in tokens:
                # Se o diretório t existir.
                if os.path.exists(t):
                    # Entre e veja se o usuário tem permissão.
                    if permissao_acesso(t, usuario):
                        os.chdir(t)
                    # Se em algum momento o usuário não tiver permissão.
                    else:
                        data['sucesso']=False
                        data['conteudo']="put: não foi possível transferir " +
                                caminho+" Permissão negada")
            # Se o usuário pode acessar todos os diretórios com permissão.
            if os.path.exists(destino):
                data['sucesso']=True
                # Se o usuário esta tentando por o arquivo em um dir..
                if os.path.isdir(destino):
                    data['conteudo']=destino + \
                        '/'+origem.split('/')[-1]
                # Se o usuário esta tentando substituir ou criar um arquivo
                # no servidor de arquivos.
                else:
                    data['conteudo']=destino
            else:
                dst=destino.split('/')
                dst.pop()
                # Se o arquivo não existir mas o diretório anterior sim
                # então crie um novo arquivo neste diretório.
                if os.path.exists('/'+'/'.join(dst)):
                    data['sucesso']=True
                    data['conteudo']=destino
                # Se o arquivo não existe o diretório também.
                else:
                    data['sucesso']=False
                    data['conteudo']="put: não foi possível transferir arquivo comum"+destino +\
                        ": Arquivo ou diretório inexistente."
        return json.dumps(data)

    def rmdir(self, caminho, json_usuario):

        usuario=User().json_loads(json_usuario)
        # Sincronizando o diretório do processo com o do usuário.
        os.chdir(usuario.dir_corrente)
        # Se o caminho for absoluto.
        if caminho[0] == '/':
            # Verificando se o usuário ter permissão no caminho
            tokens=caminho.split('/')
            # Removendo possíveis ''
            if len(tokens[-1]) == 0:
                tokens.pop()
            # Removendo caracter nulo.
            _=tokens.pop(0)
            final=tokens.pop()
            while len(tokens) > 0:
                c='/'+'/'.join(tokens)
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
                        + " Diretório não vazio.")
                else:
                    return ("rmdir: não foi possível remover"+caminho \
                        + ": Não é um diretório.")
            else:
                return ("rmdir: não foi possível remover o diretório"+c +
                        "Arquivo não encontrado.")
        # Se o caminho for relativo.
        else:
            tokens=caminho.split('/')
            # Removendo possívels ''
            if len(tokens[-1]) == 0:
                tokens.pop()
            # Removendo o nome do arquivo para poder navegar por diretórios.
            final=tokens.pop()
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
                        + " Diretório não vazio.")
                else:
                    return ("rmdir: não foi possível remover"+caminho \
                        + ": Não é um diretório.")
            else:
                return ("rmdir: não foi possível remover o diretório"+caminho +
                        "Arquivo não encontrado.")

    def rm(self, caminho):
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

    def teste(self):
        return "Servidor de arquivos funcionando corretamente."


if __name__ == '__main__':

    hostname=argv[1]
    porta=int(argv[2])
    aut=rpyc.utils.authenticators.SSLAuthenticator('certificados/no.pwd.server.key', \
        'certificados/server.crt', ssl_version=ssl.PROTOCOL_TLSv1_2)
    servidor=rpyc.ForkingServer(ServidorArquivos,
        hostname=hostname, port=porta, authenticator=aut)
    servidor.start()
