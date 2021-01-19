from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, dsa, ec, padding

from base64 import b64encode


def generate_asym_key(choice, password, folder):
    if choice == 'RSA':
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
    elif choice == 'DSA':
        private_key = dsa.generate_private_key(
            key_size=2048
        )
    elif choice == 'Elliptic Curve':
        elliptic_curve = ec.SECP384R1()
        private_key = ec.generate_private_key(elliptic_curve)

    public_key = private_key.public_key()

    serialized_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password.encode('utf-8'))
    )
    with open('utils/asymmetric/' + folder + '/private.pem', 'wb') as f:
        f.write(serialized_private_key)

    serialized_pub_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open('utils/asymmetric/' + folder + '/public.pem', 'wb') as f:
        f.write(serialized_pub_key)


def get_private(pwd, folder):
    with open("utils/asymmetric/" + folder + "/private.pem", "rb") as file:
        private_key = serialization.load_pem_private_key(
            file.read(),
            password=pwd.encode('utf-8'),
            backend=default_backend()
        )
    return private_key


def get_public(folder):
    with open("utils/asymmetric/" + folder + "/public.pem", "rb") as file:
        public_key = serialization.load_pem_public_key(
            file.read(),
            backend=default_backend()
        )
    return public_key


def save_algorithm(choice, folder, file):
    with open('utils/asymmetric/' + folder + '/' + file, 'w+') as f:
        f.write(choice)


def read_encrypted():
    with open("utils/asymmetric/encoded_message.txt", "rb") as file:
        return file.read()


def get_algorithm(folder):
    with open('utils/asymmetric/' + folder + '/encrypt.algo', 'r+') as f:
        return f.read()


def get_message():
    with open("utils/asymmetric/encoded_message.txt", "rb") as file:
        return file.read()


def get_signature():
    with open("utils/asymmetric/signature.txt", "rb") as file:
        return file.read()

def encrypt(public_key, message):
    encrypted = public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    with open('utils/asymmetric/encoded_message.txt', 'wb') as f:
        f.write(encrypted)
    return b64encode(encrypted).decode('utf-8')


def sign(private_key, choice, message):
    if choice == "RSA":
        signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    elif choice == "DSA":
        signature = private_key.sign(
            message,
            hashes.SHA256()
        )
    else:
        signature = private_key.sign(
            message,
            ec.ECDSA(hashes.SHA256())
        )
    with open('utils/asymmetric/signature.txt', 'wb') as f:
        f.write(signature)
    return b64encode(signature).decode('utf-8')

def verify():
    with open("utils/asymmetric/signing/sign.algo", "r+") as file:
        algo = file.read()
    public_key = get_public()
    if algo == "RSA":
        public_key.verify(
            get_signature(),
            get_message(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    elif algo == "DSA":
        public_key.verify(
            get_signature(),
            get_message(),
            hashes.SHA256()
        )
    else:
        public_key.verify(
            get_signature(),
            get_message(),
            ec.ECDSA(hashes.SHA256())
        )


def decrypt(pwd):
    private_key = get_private(pwd, "encryption")
    message = private_key.decrypt(
        get_message(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )).decode('utf-8')
    return message

