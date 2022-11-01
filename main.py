import socket
import sys
import select


def tcp_server(addr: str, port: int):
    with socket.socket() as s:
        s.setblocking(False)
        s.bind((addr, port))
        s.listen(5)

        inputs = {s}
        output = set()
        msgs = {}

        while True:
            readers, writers, excepts = select.select(inputs, output, inputs)
            for conn in readers:
                if conn == s:
                    conn, client_addr = s.accept()
                    conn.setblocking(False)
                    inputs.add(conn)
                    msgs[conn] = []
                    print('Connected ', client_addr)
                else:
                    data = conn.recv(1024)
                    if data:
                        msg = data
                        print(f"Msg from {conn.getpeername()}: {msg.decode('UTF-8')}")
                        msgs[conn].append(msg)
                        output.add(conn)
                    else:
                        print("Disconnected ", conn.getpeername())
                        conn.close()
                        inputs.remove(conn)
                        if conn in output:
                            output.remove(conn)
                        msgs.pop(conn, None)

            for conn in writers:
                for msg in msgs[conn]:
                    conn.sendall(msg)
                msgs[conn] = []
                output.remove(conn)

            for conn in excepts:
                inputs.remove(conn)
                if conn in output:
                    output.remove(conn)
                del msgs[conn]
                conn.close()
                print("Disconnected", conn.getpeername())


def tcp_client(addr: str, port: int):
    print("Chat with yourself")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((addr, port))
        while True:
            msg = input("> ")
            if not msg:
                break
            s.sendall(msg.encode('UTF-8'))
            data = s.recv(1024)
            print('Received', repr(data.decode("UTF-8")))


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
