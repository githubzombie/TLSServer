import socket
import ssl

HOST = "0.0.0.0"
PORT = 8443

CERT_FILE = "server.crt"
KEY_FILE = "server.key"

ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
ctx.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"TLS Echo Listening on {HOST}:{PORT} ...")

    while True:
        conn, addr = s.accept()
        print(f"TCP accepted from {addr}")
        try:
            tls_conn = ctx.wrap_socket(conn, server_side=True)
            print(f"TLS negotiated with {addr}: {tls_conn.version()}")
            while True:
                data = tls_conn.recv(1024)
                if not data:
                    print(f"TLS connection closed by {addr}")
                    break
                tls_conn.sendall(data)
        except ssl.SSLError as e:
            print(f"TLS error with {addr}: {e}")
        except ConnectionResetError:
            print(f"Connection reset by {addr}")
        finally:
            try:
                tls_conn.close()
            except Exception:
                conn.close()
