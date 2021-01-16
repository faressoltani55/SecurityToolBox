from base64 import b64encode

import streamlit as st
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, dsa, ec, padding


def asym_ecr_algorithms():
    return ["RSA", "DSA", "Elliptic Curve"]


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
    with open('utils/asymmetric/'+folder+'/private.pem', 'wb') as f:
        f.write(serialized_private_key)

    serialized_pub_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open('utils/asymmetric/'+folder+'/public.pem', 'wb') as f:
        f.write(serialized_pub_key)


def get_private(pwd, folder):
    with open("utils/asymmetric/"+folder+"/private.pem", "rb") as file:
        private_key = serialization.load_pem_private_key(
            file.read(),
            password=pwd.encode('utf-8'),
            backend=default_backend()
        )
    return private_key


def get_public(folder):
    with open("utils/asymmetric/"+folder+"/public.pem", "rb") as file:
        public_key = serialization.load_pem_public_key(
            file.read(),
            backend=default_backend()
        )
    return public_key


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


def save_algorithm(choice, folder, file):
    with open('utils/asymmetric/'+folder +'/'+file, 'w+') as f:
        f.write(choice)


def read_encrypted():
    with open("utils/asymmetric/encoded_message.txt", "rb") as file:
        return file.read()


def write():
    st.title("Here, you can chose an asymmetric encryption algorithm to encrypt / sign a message")

    choice = st.selectbox("Choose the algorithm :", asym_ecr_algorithms())

    st.text("To generate keys, you need to enter a password")
    pwd = st.text_input("Enter a password", type="password")

    funcs = ["Sign Message"]
    folders = ["signing"]
    if choice == "RSA":
        funcs.append("Encrypt Message")
        folders.append("encryption")

    folder = st.selectbox("Keys for ?", folders)

    if st.button("Generate Keys"):
        generate_asym_key(choice, pwd, folder)
        st.success("Private and Public keys generated successfully !")
        st.info("RSA is used for encryption and signing, but DSA and Elliptical Curve are used only fo signing")

    func = st.selectbox("Choose the function :", funcs)
    if func == "Sign Message":
        folder = "signing"
        save_algorithm(choice, folder, "sign.algo")
        pwd = st.text_input("Enter the password", type="password")
        if st.button("Sign"):
            try:
                private_key = get_private(pwd, folder)
                message = read_encrypted()
                res = sign(private_key, choice, message)
                st.success("Message Signed Successfully\nSignature : " + res)
            except Exception as e:
                st.error("Make sure to encode a message first\n")
                st.error(e)
    elif func == "Encrypt Message":
        folder = "encryption"
        save_algorithm(choice, folder, "encrypt.algo")
        message = st.text_input("Enter your message here")
        public_key = get_public(folder)
        res = encrypt(public_key, message)
        if st.button("Encrypt"):
            st.success("Message Encrypted Successfully\nEncryption : " + res)
