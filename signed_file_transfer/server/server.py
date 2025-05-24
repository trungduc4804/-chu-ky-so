import socket
import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key

HOST = '127.0.0.1'
PORT = 9999

with open("keys/public_key.pem", "rb") as f:
    public_key = load_pem_public_key(f.read())

os.makedirs("received_files", exist_ok=True)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"Server listening on {HOST}:{PORT}...")

while True:
    client_socket, addr = server.accept()
    print(f"Connection from {addr}")

    buffer = b""
    while b"::" not in buffer:
        buffer += client_socket.recv(1024)
    filename, buffer = buffer.split(b"::", 1)
    filename = filename.decode()

    while b"::" not in buffer:
        buffer += client_socket.recv(1024)
    signature, file_data = buffer.split(b"::", 1)
    while True:
        part = client_socket.recv(4096)
        if not part:
            break
        file_data += part

    try:
        public_key.verify(
            signature,
            file_data,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        with open(f"received_files/{filename}", "wb") as f:
            f.write(file_data)
        print(f"✔ File '{filename}' nhận thành công và chữ ký hợp lệ.")
    except Exception as e:
        print(f"❌ Chữ ký KHÔNG hợp lệ! Lỗi: {e}")

    client_socket.close()