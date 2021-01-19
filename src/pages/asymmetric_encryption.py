import streamlit as st

from src.logic.asymmetric.constants import ASYM_ALGORITHMS
from src.logic.asymmetric.functions import generate_asym_key, save_algorithm, get_private, read_encrypted, sign, \
    get_public, encrypt


def write():
    st.title("Here, you can chose an asymmetric encryption algorithm to encrypt / sign a message")

    choice = st.selectbox("Choose the algorithm :", ASYM_ALGORITHMS)

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
            st.success("Message Encrypted Successfully\nEncryption : ")
            st.text(res)