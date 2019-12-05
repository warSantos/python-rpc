import re
import ssl
import rpyc
import json
import hashlib
from base import get_opt
from sys import argv, exit


class ServidorConexeosRPC(rpyc.classic.ClassicService):

    def help(self):
        print("Ajuda.")
        print("-c: Endereço do servidor de conexões.")
        print("-f: Endereço do servidor de arquivos.")
        print("python3 src/conexoes_rpc.py -c IP -f IP")

    # Auntentica usuário no servidor de autenticação.
    def autenticar(self, login, senha, hostname="127.0.0.1", porta=8002):
        resumo = hashlib.sha256(senha.encode()).hexdigest()
        conexao = ServidorConexeosRPC().conectar(hostname, porta)
        return conexao.root.autenticar(login, resumo)

    # Abrea conexão com um servidor RPC (arquivos ou autenticação).
    # Por padrão esta definido a porta utilizada pelo servidor de arquivos
    # em testes com uma máquina apenas.
    def conectar(self, hostname="127.0.0.1", porta=8001):
        return rpyc.classic.ssl_connect(hostname, porta,
                                        ssl_version=ssl.PROTOCOL_TLSv1_2)

    # Navega entre os diretórios do usuário.
    def cd(self, conexao, caminho, usuario):
        return conexao.root.cd(caminho, usuario.usuario_json())

    def get(self, conn_clt, conexao, arquivo, usuario):
        # Verificando se o arquivo existe e se o usuário tem permissão
        # antes de iniciar o donwload do arquivo.
        data = json.loads(conexao.root.get(arquivo, usuario.usuario_json()))
        data['comando'] = 'get'
        # Se o usuário tiver permissão e o arquivo existir.
        if data['sucesso']:
            conn_clt.send(json.dumps(data).encode())
            pt = conexao.builtins.open(data['conteudo'], 'rb')
            texto = ''
            while True:
                t = pt.read(1024)
                # Se acabar o conteúdo do arquivo pare de enviar.
                if t == b'':
                    conn_clt.send('\0'.encode())
                    break
                conn_clt.send(t)
            pt.close()
        else:
            conn_clt.send(json.dumps(data).encode())

    # Lista os diretórios fazendo conexão com o servidor de arquivos.
    def ls(self, conexao, caminho, usuario):
        return conexao.root.ls(caminho, usuario.usuario_json())

    def mkdir(self, conexao, caminho, usuario):
        return conexao.root.mkdir(caminho, usuario.usuario_json())

    def put(self, conn_clt, conexao, caminhos, usuario):

        # Verificando se o diretório existe no servidor e se o usuário
        # tem permissão para escrever nele.
        data = json.loads(conexao.root.put(caminhos, usuario.usuario_json()))
        data['comando'] = 'put'
        if data['sucesso']:
            data['origem'] = caminhos[0]
            print(data)
            conn_clt.send(json.dumps(data).encode())
            retorno = json.loads(conn_clt.recv(1024))
            print(retorno)
            if retorno['confirmado']:
                # Criando arquivo no destinatário.
                pt = conexao.builtins.open(data['conteudo'], 'wb')
                while True:
                    texto = conn_clt.recv(1024)
                    if len(texto) < 1024:
                        pt.write(texto.replace(b'\x00', b''))
                        break
                    pt.write(texto)
                pt.close()
        else:
            conn_clt.send(json.dumps(data).encode())

    def rmdir(self, conexao, caminho, usuario):
        return conexao.root.rmdir(caminho, usuario.usuario_json())

    def rm(self, conexao, caminho, usuario):
        return conexao.root.rm(caminho, usuario.usuario_json())


if __name__ == "__main__":
    servidor = ServidorConexeosRPC()
    conexao = servidor.conectar("localhost", "8002")
    print(servidor.rm(conexao, "home/root/diretorio"))
