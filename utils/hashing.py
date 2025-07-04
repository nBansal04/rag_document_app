import hashlib

def compute_pdf_hash(file_bytes):
    sha256 = hashlib.sha256()
    sha256.update(file_bytes)
    return sha256.hexdigest()
