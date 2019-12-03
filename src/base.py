import os
import getopt
from sys import argv, exit

def get_opt(texto, parametros, funcao_help):
    try:
        opts, args = getopt.getopt(texto, parametros, ["help", "output="])
        dir_opts = {}
        if len(opts) == 0:
            funcao_help()
        # Construindo dicionário de parâmetros.
        for par in opts:
            if par[0] == '-h':
                funcao_help()
            dir_opts[par[0]] = par[1]
        return dir_opts
    except getopt.GetoptError as err:
        print(str(err))
        funcao_help()

def permissao_acesso(caminho, usuario):

    # Se o usuário tiver poder de root.
    if usuario.grupo_root or caminho == '':
        return True
    
    # Fazendo bkp do diretório atual.
    bkp_dir = os.getcwd()
    # Alterando o caminho para o novo diretório.
    os.chdir(caminho)
    print("Autenticação: ", os.getcwd())
    # Pegando o novo diretório.
    novo_dir = os.getcwd()
    # Retornando para o diretório anterior ao CD.
    os.chdir(bkp_dir)
    # Se o usuário não saiu de sua home.
    print("DIR padrão: ", usuario.dir_padrao)
    print("NOVO dir: ", novo_dir)
    if novo_dir.find(usuario.dir_padrao) == 0:
        return True
    return False