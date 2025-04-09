import fitz  
import requests
import io

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def download_pdf_from_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/pdf"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200 and response.headers.get("content-type", "").startswith("application/pdf"):
        return response.content
    else:
        raise Exception("Failed to download PDF. Ensure the URL directly points to a PDF file.")

def extract_text_from_url_pdf(url):
    pdf_bytes = download_pdf_from_url(url)
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text