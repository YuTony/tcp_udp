import socket
import sys
import threading


def msg_loop(conn, addr):
    with conn:
        print('Connected ', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(data.decode('UTF-8'))
            conn.sendall(data)
    print("Disconnected ", addr)


def tcp_server(addr: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((addr, port))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=msg_loop, args=(conn, addr))
            thread.start()


def tcp_client(addr: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((addr, port))
        while True:
            msg = input()
            s.sendall(msg.encode('UTF-8'))
            data = s.recv(1024)
            print('Received', repr(data))
            if data == b'\n':
                break


def udp_server(addr: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((addr, port))
        while True:
            data, client_addr = s.recvfrom(1024)
            print(f"Msg from {client_addr}: {data.decode('UTF-8')}")
            s.sendto(data, client_addr)


def udp_client(addr: str, port: int):
    print("Chat with yourself")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((addr, port))
        msg = input("> ")
        s.send(msg.encode('UTF-8'))
        data = s.recv(1024)
        print("Received", data.decode('UTF-8'))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise ValueError('3 arguments expected')
    mode, addr, port = sys.argv[1], sys.argv[2], int(sys.argv[3])
    if mode == '-ts':
        tcp_server(addr, port)
    elif mode == '-tc':
        tcp_client(addr, port)
    elif mode == '-us':
        udp_server(addr, port)
    elif mode == '-uc':
        udp_client(addr, port)
    else:
        print('Error arguments')
