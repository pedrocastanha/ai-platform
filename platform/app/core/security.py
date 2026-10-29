import hashlib
import hmac
import secrets
KEY_PREFIX = "sk_live"

def generate_api_key() -> tuple[str, str, str]:
    prefix = secrets.token_hex(4)
    secret = secrets.token_urlsafe(32)
    full_key = f"{KEY_PREFIX}_{prefix}_{secret}"

    return full_key, prefix, hash_key(full_key)

def hash_key(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()

def parse_prefix(key: str) -> str | None:
    parts = key.split("_", 3)
    if len(parts) != 4 or f"{parts[0]}_{parts[1]}" != KEY_PREFIX:
        return None
    return parts[2]

def verify_key(key: str, key_hash: str) -> bool:
    return hmac.compare_digest(hash_key(key), key_hash)
