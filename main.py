import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from encryptor import encrypt_message, decrypt_message
from dropbox_uploader import upload_to_dropbox
from email_sender import send_email_with_password
from qr_generator import generate_qr
from fpdf import FPDF
import PyPDF2
import os
from dropbox import Dropbox
import webbrowser
import threading
import time
from PIL import Image, ImageTk
import re

#  Dropbox Access Token
DROPBOX_ACCESS_TOKEN = "sl.u.AFx9LKG8Rsd3lUOClMGGPP1er1TVrSUvkkuV3KZ3DWbtGMvRLK0uIggnRbc5tM9YWKJ-0vG83aTZs8aJM9LYZvF37ZIcJ-_w8OFV7Hu4dLSuiEpwBMpVj0gISzGj6u1cV4TL1P3Cfk_jO8dwMKluhJxDk2IuVlfj8q3PtPqOnR5Q7FcaDH9WpHpzmPRTeSil0fxOuHvJc7aY-kemK64xeQfEwWXPF9nIJIBEi2yfoOur50QSbSryUwwWmh0BdvgdZmfkfkIiPnT4BiXhmF5UrR1T9UUnG3E1ECt44p79sRZFeBH16AOWFIEPs1kD188TqnDVZcxoe9_vd8AZfCj_SH7kEeefpG_aopudBWR9b_sjXPv6XToVlgKQ3lu_7WXKTvAcaGuqFoUBSrv4e5_4HT-JaA1RVy3pSphhcgYn2LDGgRuXdeXVBOrI6jcn2qhwW5egL629edaYawtNfWc7tt89nGscxmx2JJaEwda-cnm3bGpjlN9Sqmnm68LvnhoxDecLeHjTrU47ukxttIh8yr7S7SpFvMnPPLDqo-4lCa7aGWnCFL2ur9oZqq_QaMqvQ-v8c5IuYTAmaSkTXA7l7LWDBE0V6mi57x9riWPVa3fwKjRY1VT_oIjeeSsKWcOq6IxxUNIEHcBLrAz5_Bsf4S8Kkd1lagDvk-C5Z2ZJJ3bMfNuqrfEvtEH9w3Ru-NwsUgoTDbJPQfidvCVAo-gpHp9TU-dTc0G5IAsJFbmZO5dF9a_TEoubrQrSVRnkBmMs9dPKPflhklouBfl0dDnQfRaUC1dQ4BQgCXpnbn3CdkM4CjPZtxMKzmDJA0mksnHuMaBVAeOmxqQBPEcS7ORPnbK7GclkHfil95RVlF4tLdIEsWGtOn95-zpqlHW-f5eAjF7TqsSqFQ9fEWDrnOIgZOGt1Cn9eUtpl8X3xNfPur_D7TW4xhYmg9onwRlV62vXzDYhPRZpwN2Kpgd2oU1O3Ywl2FllZERVY5cv_pq9C2PfOWybeHTJmNfF3vPxHqsWKk-3Ivo69NMCmS-wCEko1cnSktRkx52TrzjpaDbOW7456QfpNa7q2g3Md-GuhrXVoLtiW5d7dISf47Skd1MtkWq659CAe2wUIu8_7WhTkMhdBRZ27kGbI1_yb_Yjq4KHY4Hb_eW1iD-oS0QkAe_3XkuBYOXoJ_ei4z4rN-Dlns6f4rKPdjcjKH7fTDF3b4f6bZb-59NXa6RPbZ1KsXJCISGB11FbaBERpM6n8_mZtwQsawtuxeIAvwSssazvXLFzj9II2Xe9UkmIb3Y5Mv8Bau2zSUT29_I_Gpm2v5EmdqNESj8eLGCdaAk8zgT5mOG6xSsFWInRZq_PK1rDNjfTi34sLdxBQdKG6QASzi6km29kH4BhurOxNYtQBmNlCGM_EOvQaD5Cj2ATH23zKqGyA64TfL2mklBcWKsT8f-7znBCgA"  # Replace with actual token

# Helper Functions 

def create_encrypted_pdf(content, filename, password):
    temp_pdf = f"temp_{filename}"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf.output(temp_pdf)

    output_pdf = PyPDF2.PdfWriter()
    reader = PyPDF2.PdfReader(temp_pdf)

    for page in reader.pages:
        output_pdf.add_page(page)

    output_pdf.encrypt(user_password=password)

    with open(filename, "wb") as f:
        output_pdf.write(f)

    os.remove(temp_pdf)


def make_link_clickable(label, url):
    def on_click(event):
        webbrowser.open_new(url)
    label.bind("<Button-1>", on_click)


def expire_qr_and_link(dropbox_path, filename, qr_path):
    time.sleep(300)  # 5 minutes

    qr_label.config(image='')
    qr_label.image = None
    link_label.config(text="⏳ QR Code and link expired.", fg="red")

    try:
        dbx = Dropbox(DROPBOX_ACCESS_TOKEN)
        dbx.files_delete_v2(dropbox_path)
    except Exception as e:
        print(f"[ERROR] Dropbox delete: {e}")

    for file in [filename, qr_path]:
        try:
            os.remove(file)
        except Exception as e:
            print(f"[ERROR] Local delete ({file}): {e}")


def is_strong_password(password):
    return (
        len(password) >= 8 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"\d", password) and
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    )

def is_valid_email(email):
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email) is not None


def handle_submit():
    global link_label

    message = message_entry.get("1.0", tk.END).strip()
    password = password_entry.get().strip()
    recipient = email_entry.get().strip()

    if not all([message, password, recipient]):
        messagebox.showerror("Error", "All fields are required!")
        return

    if not is_strong_password(password):
        messagebox.showwarning(
            "Weak Password",
            "Password must be at least 8 characters and include:\n"
            "- Uppercase letter\n- Lowercase letter\n- Digit\n- Special character"
        )
        return
    if not is_valid_email(recipient):
        messagebox.showerror("Invalid Email", "Please enter a valid email address.")
        return

    try:
        encrypted = encrypt_message(message, password)
        decrypted = decrypt_message(encrypted, password)

        pdf_filename = f"secure_{recipient.replace('@', '_at_')}.pdf"
        create_encrypted_pdf(decrypted, pdf_filename, password)

        result = upload_to_dropbox(pdf_filename)
        if isinstance(result, tuple):
            dropbox_link, dropbox_path = result
        else:
            messagebox.showerror("Dropbox Upload Failed", result)
            return

        qr_path = "qr_code.png"
        generate_qr(dropbox_link, qr_path)
        qr_image = Image.open(qr_path)
        qr_photo = ImageTk.PhotoImage(qr_image)
        qr_label.config(image=qr_photo)
        qr_label.image = qr_photo

        email_status = send_email_with_password(recipient, password)
        if email_status != "Success":
            messagebox.showwarning("Email Failed", email_status)

        link_label.config(text=f"{dropbox_link}", fg="blue", cursor="hand2")
        make_link_clickable(link_label, dropbox_link)

        messagebox.showinfo("Success", "PDF uploaded and password sent via email.")

        threading.Thread(
            target=expire_qr_and_link,
            args=(dropbox_path, pdf_filename, qr_path),
            daemon=True
        ).start()

    except Exception as e:
        messagebox.showerror("Unexpected Error", str(e))

# ------------------ GUI Setup ------------------

root = tk.Tk()
root.title("🔒 Secure PDF Generator")

root.state('zoomed')  

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

original_bg = Image.open("background.jpg") 
bg_resized = original_bg.resize((screen_width, screen_height), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_resized)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

#Style
style = ttk.Style()
style.configure('Accent.TButton', font=('Segoe UI', 12, 'bold'),
                foreground='white', background='#1e90ff', padding=8)
style.map('Accent.TButton', background=[('active', '#1c86ee'), ('pressed', '#1874cd')])
style.configure('TEntry', padding=5, relief='flat')

header_font = ("Segoe UI", 22, "bold")
label_font = ("Segoe UI", 14)
entry_font = ("Segoe UI", 12)

# Header 
top_frame = tk.Frame(root, bg="#1e90ff", height=80)
top_frame.pack(fill='x')

tk.Label(top_frame, text="🔐 Secure QR Generator",
         font=header_font, fg="black", bg="#1e90ff").pack(pady=20)

# Shadow Effect
canvas = tk.Canvas(root, width=600, height=650, bg="white", highlightthickness=0)
canvas.place(relx=0.5, rely=0.52, anchor='center')
canvas.create_rectangle(12, 12, 588, 708, fill="#bbb", outline="", stipple="gray25")

# White Frame 
form_frame = tk.Frame(canvas, bg="white", bd=0, highlightthickness=2, highlightbackground="#d3d3d3")
form_frame.place(x=0, y=0, width=576, height=620)

tk.Label(form_frame, text="Message to Encrypt", font=label_font, bg="white").pack(anchor='w', pady=(15, 5), padx=20)
message_entry = tk.Text(form_frame, height=5, width=50, font=entry_font, wrap=tk.WORD, bd=2, relief=tk.GROOVE)
message_entry.pack(pady=(0, 10), padx=20)

tk.Label(form_frame, text="Encryption Password", font=label_font, bg="white").pack(anchor='w', pady=(5, 5), padx=20)
password_entry = ttk.Entry(form_frame, show="*", width=40, font=entry_font)
password_entry.pack(pady=(0, 10), padx=20)

tk.Label(form_frame, text="Recipient Email", font=label_font, bg="white").pack(anchor='w', pady=(5, 5), padx=20)
email_entry = ttk.Entry(form_frame, width=40, font=entry_font)
email_entry.pack(pady=(0, 15), padx=20)


submit_btn = ttk.Button(form_frame, text="Encrypt & Send",style="Accent.TButton", command=handle_submit)
submit_btn.pack(pady=(5, 10))
style.configure('Accent.TButton', font=('Segoe UI', 12, 'bold'),
                foreground='black',  # <-- change to black text here
                background='#1e90ff', padding=8)
style.map('Accent.TButton', background=[('active', '#1c86ee'), ('pressed', '#1874cd')])

qr_label = tk.Label(form_frame, bg="white")
qr_label.pack(pady=(0, 3))


link_label = tk.Label(form_frame, text="", bg="white", font=("Segoe UI", 11, "underline"))
link_label.pack()

root.mainloop()