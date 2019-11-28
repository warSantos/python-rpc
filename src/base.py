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

def regex_dir(caminho):

    retornos = 2
    avancos = 0
    tokens = caminho.split('/')

    # Contabilizando os ..
    for t in tokens:
        if t == '..':
            retornos += 1
        else:
            avancos += 1
    
    # Se o caminho retorna mais na árvore que avança.
    if retornos > avancos:
        return True
    else:
        return False