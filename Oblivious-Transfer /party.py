import nacl.bindings
import nacl.secret
from oblivious import ristretto

import hashlib

def hash2point(point):
    return hashlib.blake2b(bytes(point), digest_size=32).digest()

class Sender:
    def __init__(self):
        self.secret = ristretto.scalar.random()
        self.public = ristretto.point.base(self.secret)

    def reply(self, receiver_public, msg0, msg1):
        if len(msg0) != 16 or len(msg1) != 16:
            raise ValueError("длинна сообщения не 16")

        key0 = hash2point(self.secret * receiver_public)
        key1 = hash2point(self.secret * (receiver_public - self.public))
        nonce = bytes(nacl.bindings.crypto_secretbox_NONCEBYTES)

        box0 = nacl.secret.SecretBox(key0)
        box1 = nacl.secret.SecretBox(key1)
        ct0 = box0.encrypt(msg0, nonce).ciphertext
        ct1 = box1.encrypt(msg1, nonce).ciphertext
        return ct0, ct1


class Receiver:
    def __init__(self):
        self.secret = ristretto.scalar.random()
        self.public = ristretto.point.base(self.secret)

    def query(self, sender_public, choice_bit):
        if choice_bit not in (0, 1):
            raise ValueError(r"бит не в {0, 1}")
        return self.public if choice_bit == 0 else sender_public + self.public

    def elect(self, sender_public, choice_bit, ct0, ct1):
        if choice_bit not in (0, 1):
            raise ValueError(r"бит не в {0, 1}")

        key = hash2point(self.secret * sender_public)
        box = nacl.secret.SecretBox(key)
        ciphertext = ct0 if choice_bit == 0 else ct1
        nonce_prefixed = bytes(nacl.bindings.crypto_secretbox_NONCEBYTES) + ciphertext
        return box.decrypt(nonce_prefixed)
