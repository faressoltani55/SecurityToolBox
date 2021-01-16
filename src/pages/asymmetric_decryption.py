import streamlit as st
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec, padding


def get_algorithm(folder):
    with open('utils/asymmetric/'+folder+'/encrypt.algo', 'r+') as f:
        return f.read()


def get_private(pwd, folder):
    with open("utils/asymmetric/"+folder+"/private.pem", "rb") as file:
        private_key = serialization.load_pem_private_key(
            file.read(),
            password=pwd.encode('utf-8'),
            backend=default_backend()
        )
    return private_key


def get_public():
    with open("utils/asymmetric/signing/public.pem", "rb") as file:
        public_key = serialization.load_pem_public_key(
            file.read(),
            backend=default_backend()
        )
    return public_key


def get_message():
    with open("utils/asymmetric/encoded_message.txt", "rb") as file:
        return file.read()


def get_signature():
    with open("utils/asymmetric/signature.txt", "rb") as file:
        return file.read()


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


def write():
    st.text("You can check the algorithm used for encryption here :")
    if st.button("Get Algorithm"):
        st.success("The used algorithm is " + get_algorithm("encryption"))

    func = st.selectbox("Choose the function :", ["Verify Message", "Decrypt Message"])
    if func == "Verify Message":
        if st.button("Verify"):
            try:
                verify()
                st.success("Identity Verified Successfully")
            except InvalidSignature as e:
                st.error("Identity Not verified\n" + str(e))
            except Exception as e:
                st.error("Make sure to encode and sign a message first\n" + str(e))
    elif func == "Decrypt Message":
        st.text("To decrypt a message, you need to enter a password")
        pwd = st.text_input("Enter a password", type="password")
        if st.button("Decrypt"):
            try:
                res = decrypt(pwd)
                st.success("Message Decrypted Successfully\nMessage : " + res)
            except Exception as e:
                st.error("Make sure to have an encrypted message first.\n" + str(e))
