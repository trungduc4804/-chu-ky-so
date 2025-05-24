from flask import Flask, render_template, request, flash, redirect
import socket, os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key

app = Flask(__name__)
app.secret_key = 'secret'

HOST = '127.0.0.1'
PORT = 9999

# Load private key
with open("keys/private_key.pem", "rb") as f:
    private_key = load_pem_private_key(f.read(), password=None)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file:
            filename = uploaded_file.filename
            data = uploaded_file.read()
            signature = private_key.sign(
                data,
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256()
            )
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((HOST, PORT))
                    s.sendall(filename.encode() + b"::" + signature + b"::" + data)
                flash("Gửi file thành công!", "success")
            except Exception as e:
                flash(f"Gửi thất bại: {e}", "danger")
            return redirect("/")
    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True)

