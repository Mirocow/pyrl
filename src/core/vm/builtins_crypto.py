"""
Pyrl VM Crypto Built-in Functions

Cryptographic and hashing built-in functions for the Pyrl language including:
- UUID generation (uuid)
- Hashing (sha256)
- HMAC (hmac_sha256)
- Base64 encoding/decoding (base64_encode, base64_decode)
"""
from typing import Dict


# Store for crypto built-in functions
CRYPTO_BUILTINS: Dict[str, callable] = {}


def crypto_builtin(name: str):
    """Decorator to register crypto built-in functions."""
    def decorator(func: callable) -> callable:
        CRYPTO_BUILTINS[name] = func
        return func
    return decorator


# ===========================================
# UUID Generation
# ===========================================

@crypto_builtin('uuid')
def pyrl_uuid():
    """Generate a UUID4 string.
    
    Generates a random UUID (Universally Unique Identifier) version 4.
    UUIDs are useful for generating unique identifiers for sessions,
    database records, etc.
    
    Returns:
        UUID string like '550e8400-e29b-41d4-a716-446655440000'
        
    Example:
        $session_id = uuid()
        print($session_id)  # "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d"
    """
    import uuid as uuid_module
    return str(uuid_module.uuid4())


# ===========================================
# Hashing Functions
# ===========================================

@crypto_builtin('sha256')
def pyrl_sha256(data: str):
    """Generate SHA256 hash of a string.
    
    SHA256 is a cryptographic hash function that produces a 256-bit
    (32-byte) hash value. Useful for password hashing, data integrity
    checks, and creating unique identifiers.
    
    Args:
        data: String to hash
        
    Returns:
        Hexadecimal hash string (64 characters)
        
    Example:
        $hash = sha256("hello world")
        print($hash)  # "b94d27b9934d3e08a52e52d7da7dabfa..."
    """
    import hashlib
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


@crypto_builtin('md5')
def pyrl_md5(data: str):
    """Generate MD5 hash of a string.
    
    Note: MD5 is not recommended for cryptographic purposes.
    Use SHA256 for security-sensitive applications.
    
    Args:
        data: String to hash
        
    Returns:
        Hexadecimal hash string (32 characters)
    """
    import hashlib
    return hashlib.md5(data.encode('utf-8')).hexdigest()


# ===========================================
# HMAC Functions
# ===========================================

@crypto_builtin('hmac_sha256')
def pyrl_hmac_sha256(key: str, message: str):
    """Generate HMAC-SHA256 hash.
    
    HMAC (Hash-based Message Authentication Code) provides a way to
    verify both the integrity and authenticity of a message. Useful
    for API signature verification and secure message transmission.
    
    Args:
        key: Secret key for HMAC
        message: Message to hash
        
    Returns:
        Hexadecimal hash string (64 characters)
        
    Example:
        $signature = hmac_sha256("secret_key", "message to sign")
    """
    import hmac
    import hashlib
    return hmac.new(
        key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()


@crypto_builtin('hmac_md5')
def pyrl_hmac_md5(key: str, message: str):
    """Generate HMAC-MD5 hash.
    
    Note: HMAC-MD5 is not recommended for cryptographic purposes.
    Use HMAC-SHA256 for security-sensitive applications.
    
    Args:
        key: Secret key for HMAC
        message: Message to hash
        
    Returns:
        Hexadecimal hash string (32 characters)
    """
    import hmac
    import hashlib
    return hmac.new(
        key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.md5
    ).hexdigest()


# ===========================================
# Base64 Functions
# ===========================================

@crypto_builtin('base64_encode')
def pyrl_base64_encode(data: str):
    """Encode string to base64.
    
    Base64 encoding converts binary data into ASCII characters that
    can be safely transmitted over text-based protocols.
    
    Args:
        data: String to encode
        
    Returns:
        Base64 encoded string
        
    Example:
        $encoded = base64_encode("Hello, World!")
        print($encoded)  # "SGVsbG8sIFdvcmxkIQ=="
    """
    import base64
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')


@crypto_builtin('base64_decode')
def pyrl_base64_decode(data: str):
    """Decode base64 string.
    
    Decodes a base64-encoded string back to its original form.
    
    Args:
        data: Base64 encoded string
        
    Returns:
        Decoded string
        
    Example:
        $decoded = base64_decode("SGVsbG8sIFdvcmxkIQ==")
        print($decoded)  # "Hello, World!"
    """
    import base64
    return base64.b64decode(data.encode('utf-8')).decode('utf-8')


@crypto_builtin('base64_url_encode')
def pyrl_base64_url_encode(data: str):
    """Encode string to URL-safe base64.
    
    URL-safe base64 encoding replaces '+' with '-' and '/' with '_',
    making the output safe for use in URLs.
    
    Args:
        data: String to encode
        
    Returns:
        URL-safe base64 encoded string
    """
    import base64
    return base64.urlsafe_b64encode(data.encode('utf-8')).decode('utf-8')


@crypto_builtin('base64_url_decode')
def pyrl_base64_url_decode(data: str):
    """Decode URL-safe base64 string.
    
    Args:
        data: URL-safe base64 encoded string
        
    Returns:
        Decoded string
    """
    import base64
    return base64.urlsafe_b64decode(data.encode('utf-8')).decode('utf-8')


# ===========================================
# Hex Functions
# ===========================================

@crypto_builtin('hex_encode')
def pyrl_hex_encode(data: str):
    """Encode string to hexadecimal.
    
    Args:
        data: String to encode
        
    Returns:
        Hexadecimal encoded string
    """
    return data.encode('utf-8').hex()


@crypto_builtin('hex_decode')
def pyrl_hex_decode(data: str):
    """Decode hexadecimal string.
    
    Args:
        data: Hexadecimal encoded string
        
    Returns:
        Decoded string
    """
    return bytes.fromhex(data).decode('utf-8')
