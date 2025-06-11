# 🔐 Secure QR Code and Password-Protected PDF Generator

This project proposes a secure and efficient system for password-protected QR code generation using Python and Tkinter. It allows users to input confidential data, encrypt it, and generate a QR code or a password-protected PDF for secure sharing. To ensure convenience and security, Dropbox cloud integration and an expiry mechanism for temporary access are included.

---

## 💡 Features

- ✅ User-friendly GUI (built with Tkinter)
- 🔒 Encrypts sensitive text input
- 📄 Generates password-protected PDF files
- 📷 Generates secure QR codes
- ☁️ Uploads files to Dropbox and returns shareable links
- ⏳ Expiry time mechanism for auto-deleting or expiring shared links

---

## 🛠️ Technologies Used

| Technology      | Why It’s Used                                                                 |
|-----------------|--------------------------------------------------------------------------------|
| **Python**      | Core programming language for logic and backend operations                    |
| **Tkinter**     | To build a simple, interactive, and user-friendly desktop GUI                 |
| **qrcode**      | For generating secure QR codes                                                |
| **reportlab**   | For creating password-protected PDF documents                                 |
| **dropbox**     | To upload generated files to Dropbox and retrieve shareable links             |
| **cryptography**| To encrypt the data before embedding in QR or PDF, ensuring confidentiality   |

---

## 📷 Screenshot

![App Screenshot](7051ff02-28e3-476c-83ac-d579c23a8d4c.png)

---

## 🧪 How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/secure-qr-generator.git
   cd secure-qr-generator
2. **Create DropBox Account**
   Create an app in drop box and generate the token and change that in code.
   Create app in gmail and also cahnge app password in code.
