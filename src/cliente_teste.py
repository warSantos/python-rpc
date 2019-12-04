import sys
import rpyc
import socket
from rpyc.core.stream import SocketStream
from sys import argv, exit

if __name__ == '__main__':

    hostname = argv[1]
    porta = argv[2]

    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.bind(("localhost", 8005))
    sock_stream = SocketStream(s)
    conn = rpyc.connect_pipes(sock_stream, sys.stdout)
    print(conn.root.get())
    #print(conn.root.get())
    """
    
    #print(conn.root.get())

    #conn = rpyc.connect(hostname, porta)
    #conn = rpyc.utils.classic.connect(hostname, porta)
    #s = SocketStream.connect(hostname, porta)
    #conn = rpyc.connect_stream(s)
    conn = rpyc.utils.classic.connect(hostname, porta)
    #conn.root.get()
    print(dir(conn))
    
    """
    conn = rpyc.utils.classic.connect(hostname, porta)
    rpyc.utils.classic.download_file(conn, '/home/user/temp/RAW_interactions.csv', \
        './file')
    """