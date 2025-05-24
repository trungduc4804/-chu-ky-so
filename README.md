# Ứng dụng Truyền File Dữ Liệu Có Ký Số (Digital Signature)

## 📌 Mô tả

Ứng dụng cho phép người dùng gửi file từ client (giao diện web) đến server. Trước khi gửi, file được **ký số bằng khóa riêng (private key)**. Server sẽ:
- **Xác minh chữ ký bằng khóa công khai (public key)**
- **Chấp nhận hoặc từ chối** file tùy vào chữ ký hợp lệ hay không

Việc này giúp đảm bảo:
- Tính **toàn vẹn** của file (file không bị thay đổi)
- Tính **xác thực** (biết chắc người gửi là ai)

---

## 📁 Cấu trúc thư mục

```
signed-file-transfer/
├── client/
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   └── keys/
│       └── private_key.pem
├── server/
│   ├── server.py
│   ├── keys/
│   │   └── public_key.pem
│   └── received_files/
├── gen_keys.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Cài đặt

### 1. Cài thư viện cần thiết

```bash
pip install -r requirements.txt
```

**Nội dung `requirements.txt`:**

```
flask
cryptography
```

### 2. Tạo cặp khóa RSA

```bash
python gen_keys.py
```

File tạo ra:
- `private_key.pem` → dùng ở **client**
- `public_key.pem` → dùng ở **server**

---

## ▶️ Cách chạy chương trình

### Bước 1: Khởi động server

```bash
cd server
python server.py
```

### Bước 2: Khởi động client web

```bash
cd client
python app.py
```

→ Truy cập trình duyệt tại: http://127.0.0.1:5000

### Bước 3: Gửi file

- Chọn file từ giao diện web
- Gửi file
- Xem kết quả:
  - Nếu hợp lệ: server lưu file và in ra thông báo thành công
  - Nếu sai chữ ký: từ chối và báo lỗi

---

## 🛡️ Công nghệ sử dụng

- **Flask** – xây dựng giao diện web cho client
- **Socket** – truyền dữ liệu giữa client và server
- **Cryptography (Python)** – tạo và xác minh chữ ký số (RSA + SHA-256)

---

## 🧪 Kiểm tra thành công

Khi gửi file thành công:
- Trên web: thông báo "Gửi file thành công!"
- Trên server: xuất hiện dòng `✔ File 'tên_file' nhận thành công và chữ ký hợp lệ.`
- File sẽ được lưu trong `server/received_files/`
