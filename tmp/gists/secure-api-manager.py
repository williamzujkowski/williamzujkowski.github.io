import os
from cryptography.fernet import Fernet
import keyring
from typing import Optional

class SecureAPIManager:
    """Manage API keys securely using encryption and system keyring."""

    def __init__(self, service_name: str = "homelab-ai"):
        self.service_name = service_name
        self.cipher_key = self._get_or_create_cipher_key()
        self.cipher = Fernet(self.cipher_key)

    def _get_or_create_cipher_key(self) -> bytes:
        """Get encryption key from system keyring or create new one."""
        key = keyring.get_password(self.service_name, "cipher_key")
        if not key:
            key = Fernet.generate_key().decode()
            keyring.set_password(self.service_name, "cipher_key", key)
        return key.encode()

    def store_api_key(self, key_name: str, api_key: str) -> None:
        """Encrypt and store API key."""
        encrypted_key = self.cipher.encrypt(api_key.encode())
        keyring.set_password(self.service_name, key_name, encrypted_key.decode())

    def get_api_key(self, key_name: str) -> Optional[str]:
        """Retrieve and decrypt API key."""
        encrypted_key = keyring.get_password(self.service_name, key_name)
        if not encrypted_key:
            return None
        return self.cipher.decrypt(encrypted_key.encode()).decode()

    def rotate_key(self, key_name: str, new_api_key: str) -> None:
        """Rotate API key."""
        self.store_api_key(key_name, new_api_key)
