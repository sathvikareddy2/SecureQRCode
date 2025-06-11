from cryptography.fernet import Fernet
import base64
import hashlib

def get_fernet(password):
    key = hashlib.sha256(password.encode()).digest()
    fernet_key = base64.urlsafe_b64encode(key[:32])
    return Fernet(fernet_key)

def encrypt_message(message, password):
    fernet = get_fernet(password)
    return fernet.encrypt(message.encode()).decode()

def decrypt_message(encrypted_text, password):
    fernet = get_fernet(password)
    return fernet.decrypt(encrypted_text.encode()).decode()
