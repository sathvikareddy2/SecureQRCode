from fpdf import FPDF
import PyPDF2
import os

def create_encrypted_pdf(content, filename, password):
    temp_pdf = f"temp_{filename}"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf.output(temp_pdf)

    writer = PyPDF2.PdfWriter()
    reader = PyPDF2.PdfReader(temp_pdf)

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(user_password=password)  
    with open(filename, "wb") as f:
        writer.write(f)

    os.remove(temp_pdf)
