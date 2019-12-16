import os
import getopt
import pymysql
from sys import argv, exit

def get_opt(texto, parametros, funcao_help):
    try:
        opts, args = getopt.getopt(texto, parametros, ["help", "output="])
        dir_opts = {}
        if len(opts) == 0:
            funcao_help()
            exit(1)
        # Construindo dicionário de parâmetros.
        for par in opts:
            if par[0] == '-h':
                funcao_help()
                exit(1)
            dir_opts[par[0]] = par[1]
        return dir_opts
    except getopt.GetoptError as err:
        print(str(err))
        funcao_help()
        exit(1)

def permissao_acesso(caminho, usuario):

    # Se o usuário tiver poder de root.
    if usuario.grupo_root or caminho == '':
        return True
    
    # Fazendo bkp do diretório atual.
    bkp_dir = os.getcwd()
    # Alterando o caminho para o novo diretório.
    os.chdir(caminho)
    # Pegando o novo diretório.
    novo_dir = os.getcwd()
    # Retornando para o diretório anterior ao CD.
    os.chdir(bkp_dir)
    # Se o usuário não saiu de sua home.
    if novo_dir.find(usuario.dir_padrao) == 0:
        return True
    return False

def mysql_conn():
    
    return pymysql.connect("localhost","root","rootroot","logins")

def mysql_select_user(login=None):

    if login is None:
        return False
    
    db = mysql_conn()    
    cursor = db.cursor()
    sql = "SELECT * FROM usuarios WHERE login = '" + login + "';"
    result = cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    return result

def mysql_insert_user(login, resumo, grupo_root):

    db = mysql_conn()    
    cursor = db.cursor()
    sql = "INSERT INTO usuarios(login, senha, grupo_root) VALUES "+\
    "('"+login+"', '"+resumo+"', "+str(grupo_root)+")"
    cursor.execute(sql)
    db.commit()
    db.close()