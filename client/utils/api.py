import requests
from config import API_URL

def upload_pdfs_api(files):
    files_payload=[("files", (f.name, f.read(), "application/pdf")) for f in files]
    response = requests.post(
        f"{API_URL}/upload_pdfs",
        files=files_payload
    )
    return response

def ask_question(question):
    response = requests.post(
        f"{API_URL}/ask",
        data={"question": question}
    )
    return response
