import base64

import os

from cryptography.exceptions import InvalidKey, AlreadyFinalized
from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

from utils.symmetric.algorithms import SYM_ALGORITHMS_PROPS

ALGORITHM_PADDING = 256
SCRYPT_BLOCK_SIZE_PARAMETER = 8
SCRYPT_PARALLELIZATION_PARAMETER = 1
SCRYPT_COST_PARAMETER = 2 ** 14
SYM_KEY_PATH = 'utils/symmetric/keys/secret.key'

def reset_key():
    try:
        os.remove(SYM_KEY_PATH)
    except OSError as error:
        print(error)
        return False
    return True

def get_key_sizes(algorithm):
    return SYM_ALGORITHMS_PROPS[algorithm]['key_sizes']

def generate_secret_key(size, password):

    salt = os.urandom(16)
    # derive key
    kdf = Scrypt(salt = salt, length = int(size / 8), n = SCRYPT_COST_PARAMETER, r = SCRYPT_BLOCK_SIZE_PARAMETER, p = SCRYPT_PARALLELIZATION_PARAMETER)
    key = kdf.derive(bytes(password, encoding='utf-8'))

    with open(SYM_KEY_PATH, 'wb') as f:
        f.write(salt+key)
    return key

def upload_secret_key(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.read()
        with open(SYM_KEY_PATH, 'wb') as f:
            f.write(bytes_data)
        return True
    else:
        return False

def verify_secret_key(password):

    try:
        with open(SYM_KEY_PATH, "rb") as file:
            salt_and_key = file.read()
    except FileNotFoundError:
        return False, "No secret key found"

    salt = salt_and_key[:16]
    key = salt_and_key[16:]
    length = len(key)

    kdf = Scrypt(salt = salt, length = length, n = SCRYPT_COST_PARAMETER, r = SCRYPT_BLOCK_SIZE_PARAMETER, p = SCRYPT_PARALLELIZATION_PARAMETER)
    try:
        kdf.verify(bytes(password, encoding='utf-8'), key)
    except InvalidKey:
        return False, "Invalid key", None
    except AlreadyFinalized:
        return False, "Error was encountered during the verification process", None

    return True, "Password successfully verified", key


def get_key():
    try:
        with open(SYM_KEY_PATH, "rb") as file:
            return file.read()
    except:
        return None


def download_secret_key(key):
    b64 = base64.b64encode(key).decode()
    href = f'<a href="data:file;base64,{b64}">Download Key File</a> (right-click and save as secret.key)'
    return href


def encrypt(algorithm, key, message):
    algo = getattr(algorithms, algorithm)
    block_size = SYM_ALGORITHMS_PROPS[algorithm]['block_size']
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


def algorithm_strength(algorithm):
    return  SYM_ALGORITHMS_PROPS[algorithm]['strength']


def decrypt(password, cipher_text_encoded):

    cipher_text_decoded = base64.b64decode(cipher_text_encoded)

    algorithm = get_algorithm(cipher_text_encoded)
    algo = getattr(algorithms, algorithm)
    block_size_bytes = int(SYM_ALGORITHMS_PROPS[algorithm]['block_size']/8)
    algorithm_padding_bytes = int(ALGORITHM_PADDING/8)
    iv = cipher_text_decoded[algorithm_padding_bytes:algorithm_padding_bytes+block_size_bytes]
    cipher_text = cipher_text_decoded[algorithm_padding_bytes + block_size_bytes:]

    verified, info_message, key = verify_secret_key(password)

    if verified:
        cipher = Cipher(algo(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted_padded_message = decryptor.update(cipher_text) + decryptor.finalize()
        message_unpadder = padding.PKCS7(block_size_bytes * 8).unpadder()
        decrypted_message = message_unpadder.update(decrypted_padded_message) + message_unpadder.finalize()
        return True, decrypted_message.decode('utf-8')

    else:
        False, info_message
