import torch
import hashlib
from pathlib import Path
from typing import Optional

class SecureModelLoader:
    """Verify model integrity before loading."""

    def __init__(self, trusted_hashes_file: str = "model_hashes.txt"):
        self.trusted_hashes = self._load_trusted_hashes(trusted_hashes_file)

    def _load_trusted_hashes(self, filepath: str) -> dict:
        """Load known-good model checksums."""
        hashes = {}
        if Path(filepath).exists():
            with open(filepath, 'r') as f:
                for line in f:
                    model_name, checksum = line.strip().split(':')
                    hashes[model_name] = checksum
        return hashes

    def verify_model(self, model_path: Path) -> bool:
        """Verify model hasn't been tampered with."""
        sha256_hash = hashlib.sha256()
        with open(model_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        computed_hash = sha256_hash.hexdigest()
        expected_hash = self.trusted_hashes.get(model_path.name)

        if expected_hash and computed_hash != expected_hash:
            raise ValueError(f"Model checksum mismatch: {model_path.name}")

        return True

    def load_safe_model(self, model_path: Path) -> Optional[torch.nn.Module]:
        """Load model only after verification."""
        self.verify_model(model_path)
        return torch.load(model_path, map_location='cpu')

    def sanitize_input(self, user_input: str) -> str:
        """Basic input sanitization."""
        sanitized = user_input.strip()
        # Remove potential path traversal attempts
        sanitized = sanitized.replace('../', '').replace('..\\', '')
        # Add more sanitization as needed
        return sanitized
