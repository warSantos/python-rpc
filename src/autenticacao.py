import re
import ssl
import rpyc
import json
import hashlib
from sys import argv, exit

# Importando módulos locais.
#from base import get_opt

class ServidorAutenticacao(rpyc.classic.ClassicService):

    def ajuda(self):
        print("Ajuda.")
        print("-c: Endereço do servidor de conexões.")
        print("-f: Endereço do servidor de arquivos.")
        print("python3 src/conexoes_rpc.py -c IP -f IP")

    def criarUsuario(self, login, senha):

        if login == '' or senha == '':
            return ("O usuário e a senha não podem ser vazios.")
        if len(login) > 50:
            print("O login deve conter no máximo 50 caracteres.")
            return ("O login deve conter no máximo 50 caracteres.")
        else:
            # Verificando se o login contém caracteres especiais.
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
            if regex.search(login) != None:
                print("O login deve conter somente letras e números.")
                return ("O login deve conter somente letras e números.")
            # Verificando se o login já existe na base de dados.
            pt = open('banco/logins.txt', 'r')
            for tupla in pt:
                usuario, senha = tupla.split(':')
                if usuario == login:
                    print("Este login já foi tomando.")
                    return ("Este login já foi tomado.")
            pt.close()
            # Persistindo o usuário no disco.
            pt = open('banco/logins.txt', 'a')
            pt.write(login+':'+hashlib.sha256(senha.encode()).hexdigest()+'\n')
            pt.close()

            # Criando home do usuário.
            conexao = rpyc.connect('127.0.0.1', '8002')
            print(conexao.root.criarHome(login))
            print("Usuário: "+login+" pronto para uso.")

    # Converte um dicionário de autenticação em um json string.
    def encode_aut(self, conteudo, aceito=False, perm=False):

        data = {}
        data['conteudo'] = conteudo
        data['aceito'] = aceito
        data['grupo_root'] = perm
        return json.dumps(data)

    # TODO: verificar se realmente vai percisar desse método.
    def decode_aut(self, texto):
        json.loads(texto)

    def autenticar(self, login, resumo):
        
        if login == '' or resumo == '':
            print("O usuário e a senha não podem ser vazios.")
            data = ServidorAutenticacao().encode_aut( \
                "O usuário e a senha não podem ser vazios.")
            return data
        if len(login) > 50:
            data = ServidorAutenticacao().encode_aut( \
                "O login deve conter no máximo 50 caracteres.")
            return data
        else:
            # Verificando se o login contém caracteres especiais.
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
            if regex.search(login) != None:
                data = ServidorAutenticacao().encode_aut( \
                "O login deve conter somente letras e números.")
                return data
            pt = open('banco/logins.txt', 'r')
            for tupla in pt:
                usuario, resumo_bd, grupo_root = tupla.split(':')
                # Verificando se o login existe na base de dados.
                if usuario == login:
                    # Se o usuário existir compare a senha dele.
                    if resumo == resumo_bd.replace('\n',''):
                        perm_root =  False
                        if grupo_root == 'True':
                            perm_root = True
                        data = ServidorAutenticacao().encode_aut( \
                            "Usuário autenticado.", True, perm_root)
                        return data
                    else:
                        data = ServidorAutenticacao().encode_aut( \
                            "Falha na aunteticação. Senha incorreta.")
                        return data
            pt.close()
            data = ServidorAutenticacao().encode_aut( \
                "Falha na autenticação. Usário inexistente.")
            return data

    def teste(self):
        return "Servidor de autenticação funcionando corretamente."

if __name__=='__main__':

    #opts = get_opt(argv[1:], "c:f:", ServidorAutenticacao().ajuda)

    # Pegando o IP dos servidores de arquivos e de conexão.
    #ip_scon = opts['-c']
    #ip_sarq = opts['-f']

    hostname = '0.0.0.0'
    porta = 8002

    #servidor = ServidorAutenticacao()
    if hostname == 'root':
        servidor.criarUsuario(hostname, argv[2])
    else:
        aut = rpyc.utils.authenticators.SSLAuthenticator( \
            'certificados/no.pwd.server.key', \
            'certificados/server.crt', ssl_version=ssl.PROTOCOL_TLSv1_2)
        servidor = rpyc.ForkingServer(ServidorAutenticacao, \
            hostname=hostname, port=porta, authenticator=aut)
        servidor.start()