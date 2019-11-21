import re
import rpyc
import hashlib
from sys import argv, exit

class ServidorAutenticacao(rpyc.Service):

    def exposed_criarUsuario(self, login, senha):

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

    def exposed_autenticar(self):
        print("Autenticado.")

    def exposed_teste(self):
        return "Servidor de autenticação funcionando corretamente."

if __name__=='__main__':

    hostname = argv[1]
    if hostname == 'root':
        servidor = ServidorAutenticacao()
        servidor.exposed_criarUsuario(hostname, argv[2])
    else:
        porta = int(argv[2])
        servidor = rpyc.ThreadPoolServer(ServidorAutenticacao, \
            hostname=hostname, port=porta)
        servidor.start()
