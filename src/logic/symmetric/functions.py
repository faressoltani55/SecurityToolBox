import base64

import os

from cryptography.exceptions import InvalidKey, AlreadyFinalized
from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

ALGORITHM_PADDING = 256
SCRYPT_BLOCK_SIZE_PARAMETER = 8
SCRYPT_PARALLELIZATION_PARAMETER = 1
SCRYPT_COST_PARAMETER = 2 ** 14


def get_key_sizes(algorithm):
    algorithm_class = getattr(algorithms, algorithm)
    return list(algorithm_class.key_sizes)


def generate_secret_key(size, password):

    salt = os.urandom(16)
    # derive key
    kdf = Scrypt(salt = salt, length = int(size / 8), n = SCRYPT_COST_PARAMETER, r = SCRYPT_BLOCK_SIZE_PARAMETER, p = SCRYPT_PARALLELIZATION_PARAMETER)
    key = kdf.derive(bytes(password, encoding='utf-8'))

    with open('utils/symmetric/keys/secret.key', 'wb') as f:
        f.write(key)
    with open('utils/symmetric/keys/secret.salt', 'wb') as f:
        f.write(salt)
    return key


def verify_secret_key(password):

    try:
        with open("utils/symmetric/keys/secret.key", "rb") as file:
            key = file.read()
        with open("utils/symmetric/keys/secret.salt", "rb") as file:
            salt = file.read()
    except FileNotFoundError:
        return False, "No secret keys found"

    length = len(key)
    kdf = Scrypt(salt = salt, length = length, n = SCRYPT_COST_PARAMETER, r = SCRYPT_BLOCK_SIZE_PARAMETER, p = SCRYPT_PARALLELIZATION_PARAMETER)
    try:
        kdf.verify(bytes(password, encoding='utf-8'), key)
    except InvalidKey:
        return False, "Invalid key"
    except AlreadyFinalized:
        return False, "Error was encountered during the verification process"

    return True, "Password successfully verified"


def get_key():
    try:
        with open("utils/symmetric/keys/secret.key", "rb") as file:
            return file.read()
    except FileNotFoundError:
        return None


def download_encrypted_message(message):
    b64 = base64.b64encode(message).decode()
    href = f'<a href="data:file/bin;base64,{b64}">Download Encrypted Message File</a> (right-click and save as &lt;some_name&gt;.bin)'
    return href


def write_encrypted_file(path, cipher_text, metadata):
    with open('utils/symmetric/encoded_message.txt', 'wb') as f:
        f.write(cipher_text)


def read_encrypted_file(path):
    with open("utils/symmetric/encoded_message.txt", "rb") as file:
        return file.read()


def encrypt(algorithm, key, message):
    algo = getattr(algorithms, algorithm)
    block_size = algo.block_size
    block_size_bytes = int(block_size / 8)

    iv = os.urandom(block_size_bytes)
    cipher = Cipher(algo(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    message_padder = padding.PKCS7(block_size).padder()
    padded_message = message_padder.update(bytes(message, encoding='utf-8')) + message_padder.finalize()

    algorithm_padder = padding.PKCS7(ALGORITHM_PADDING).padder()
    padded_algorithm = algorithm_padder.update(bytes(algorithm, encoding='utf-8')) + algorithm_padder.finalize()

    cipher_text = encryptor.update(padded_message) + encryptor.finalize()
    cipher_text_encoded = base64.b64encode(padded_algorithm + iv + cipher_text).decode('utf-8')

    return cipher_text_encoded


def get_algorithm(cipher_text_encoded):

    cipher_text_decoded = base64.b64decode(cipher_text_encoded)
    algorithm_unpadder = padding.PKCS7(ALGORITHM_PADDING).unpadder()
    algorithm = algorithm_unpadder.update(cipher_text_decoded[:int(ALGORITHM_PADDING / 8)]) + algorithm_unpadder.finalize()

    return algorithm.decode('utf-8')


def decrypt(password, cipher_text_encoded):

    cipher_text_decoded = base64.b64decode(cipher_text_encoded)

    algorithm = get_algorithm(cipher_text_encoded)
    algo = getattr(algorithms, algorithm)
    block_size_bytes = int(getattr(algorithms, algorithm).block_size/8)
    algorithm_padding_bytes = int(ALGORITHM_PADDING/8)
    iv = cipher_text_decoded[algorithm_padding_bytes:algorithm_padding_bytes+block_size_bytes]
    cipher_text = cipher_text_decoded[algorithm_padding_bytes + block_size_bytes:]

    verified, info_message = verify_secret_key(password)

    if verified:
        key = get_key()
        cipher = Cipher(algo(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted_padded_message = decryptor.update(cipher_text) + decryptor.finalize()
        message_unpadder = padding.PKCS7(block_size_bytes * 8).unpadder()
        decrypted_message = message_unpadder.update(decrypted_padded_message) + message_unpadder.finalize()
        return True, decrypted_message.decode('utf-8')

    else:
        False, info_message
