import os
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

CLASSIFICATION_ACTIONS = {
    "Public":       {"hide": True, "encrypt": False, "password": False},
    "Restricted":   {"hide": True, "encrypt": True,  "password": True},
    "Confidential": {"hide": True, "encrypt": True,  "password": True},
}

_KEY_FILE = "key.key"
_salt = b"adaptive_stego_salt_v1"


def _get_or_create_key():

    if not os.path.exists(_KEY_FILE):
        key = Fernet.generate_key()
        with open(_KEY_FILE, "wb") as key_file:
            key_file.write(key)
    with open(_KEY_FILE, "rb") as key_file:
        return key_file.read()


def _derive_key_from_password(password: str) -> bytes:

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=_salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def encrypt(message: str, level: str, password: str = None):

    actions = CLASSIFICATION_ACTIONS.get(level, CLASSIFICATION_ACTIONS["Restricted"])
    if not actions["encrypt"]:
        return {"encrypted": False, "data": message, "level": level}

    if actions["password"] and password:
        key = _derive_key_from_password(password)
        cipher = Fernet(key)
    else:
        key = _get_or_create_key()
        cipher = Fernet(key)

    encrypted_message = cipher.encrypt(message.encode())
    return {"encrypted": True, "data": encrypted_message, "level": level}


def decrypt(encrypted_data, password: str = None):
    
    level = encrypted_data.get("level", "Restricted")
    actions = CLASSIFICATION_ACTIONS.get(level, CLASSIFICATION_ACTIONS["Restricted"])
    if not actions["encrypt"]:
        return encrypted_data["data"] if isinstance(encrypted_data["data"], str) else encrypted_data["data"].decode()

    if actions["password"] and password:
        key = _derive_key_from_password(password)
        cipher = Fernet(key)
    else:
        key = _get_or_create_key()
        cipher = Fernet(key)

    data = encrypted_data["data"]
    if isinstance(data, str):
        data = data.encode()
    decrypted_message = cipher.decrypt(data).decode()
    return decrypted_message
