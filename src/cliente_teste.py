import rpyc
from sys import argv, exit

if __name__=='__main__':

    hostname = argv[1]
    porta = argv[2]
    conn = rpyc.connect(hostname, porta)
    print(conn.root.teste())