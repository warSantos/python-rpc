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