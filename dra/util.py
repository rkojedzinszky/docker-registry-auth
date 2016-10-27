
import hashlib
import base64
import re
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from django.utils.functional import cached_property

class PrivateKey(object):
    """ This represents a private key used in
    JWT signatures with 'kid' field generation """
    def __init__(self, path):
        self._path = path

    @cached_property
    def key(self):
        with open(self._path, 'rb') as h:
            return serialization.load_pem_private_key(h.read(), password=None, backend=default_backend())

    @cached_property
    def public_key(self):
        return self.key.public_key()

    @cached_property
    def public_key_kid(self):
        der_bytes = self.public_key.public_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
        hasher = hashlib.sha256()
        hasher.update(der_bytes)
        digest = hasher.digest()
        b32 = base64.b32encode(digest[0:30])

        return ':'.join(re.findall('.{4}', b32))
