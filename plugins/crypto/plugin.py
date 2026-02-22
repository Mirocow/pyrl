# FILE: plugins/crypto/plugin.py
"""
Crypto Plugin for Pyrl
Provides cryptographic and hashing functions
"""

from pyrl_plugin_system import PluginBase
import hashlib
import base64
import secrets
import string
import hmac


class CryptoPlugin(PluginBase):
    """Cryptographic functions"""
    
    NAME = "crypto"
    VERSION = "1.0.0"
    DESCRIPTION = "Cryptographic and hashing functions"
    AUTHOR = "Pyrl Ecosystem Team"
    
    def on_load(self):
        """Register crypto functions"""
        self.register_function("md5", self._md5)
        self.register_function("sha1", self._sha1)
        self.register_function("sha256", self._sha256)
        self.register_function("sha512", self._sha512)
        self.register_function("hmac_sha256", self._hmac_sha256)
        self.register_function("base64_encode", self._base64_encode)
        self.register_function("base64_decode", self._base64_decode)
        self.register_function("uuid", self._uuid)
        self.register_function("uuid_v4", self._uuid_v4)
        self.register_function("random_string", self._random_string)
        self.register_function("random_int", self._random_int)
        self.register_function("random_hex", self._random_hex)
        self.log("Crypto functions loaded")
    
    def _md5(self, s):
        """MD5 hash"""
        return hashlib.md5(s.encode()).hexdigest()
    
    def _sha1(self, s):
        """SHA1 hash"""
        return hashlib.sha1(s.encode()).hexdigest()
    
    def _sha256(self, s):
        """SHA256 hash"""
        return hashlib.sha256(s.encode()).hexdigest()
    
    def _sha512(self, s):
        """SHA512 hash"""
        return hashlib.sha512(s.encode()).hexdigest()
    
    def _hmac_sha256(self, key, message):
        """HMAC-SHA256"""
        return hmac.new(
            key.encode() if isinstance(key, str) else key,
            message.encode() if isinstance(message, str) else message,
            hashlib.sha256
        ).hexdigest()
    
    def _base64_encode(self, s):
        """Base64 encode"""
        if isinstance(s, str):
            s = s.encode()
        return base64.b64encode(s).decode()
    
    def _base64_decode(self, s):
        """Base64 decode"""
        return base64.b64decode(s).decode()
    
    def _uuid(self):
        """Generate UUID v4"""
        import uuid
        return str(uuid.uuid4())
    
    def _uuid_v4(self):
        """Generate UUID v4 (alias)"""
        return self._uuid()
    
    def _random_string(self, length=16, chars=None):
        """Generate random string"""
        if chars is None:
            chars = string.ascii_letters + string.digits
        return ''.join(secrets.choice(chars) for _ in range(length))
    
    def _random_int(self, min_val=0, max_val=1000000):
        """Generate random integer in range"""
        return secrets.randbelow(max_val - min_val + 1) + min_val
    
    def _random_hex(self, length=32):
        """Generate random hex string"""
        return secrets.token_hex(length // 2)


# Export plugin class
plugin_class = CryptoPlugin
