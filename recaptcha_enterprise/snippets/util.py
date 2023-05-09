import hashlib
import hmac
import secrets


def _get_hashed_account_id(account_id: str, key: str) -> str:
    salt = secrets.token_hex(16)
    salted_account_id = salt + account_id

    # Encode the key and salted message as bytes
    key_bytes = bytes(key, 'utf-8')
    salted_message_bytes = bytes(salted_account_id, 'utf-8')

    # Create an HMAC SHA-256 hash of the salted message using the key
    hashed = hmac.new(key_bytes, salted_message_bytes, hashlib.sha256)

    # Get the hex-encoded digest of the hash
    return hashed.hexdigest()
