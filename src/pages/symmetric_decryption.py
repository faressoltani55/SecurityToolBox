import utils.symmetric.algorithms as sym_utils
import streamlit as st

from src.logic.symmetric.functions import get_algorithm, decrypt


def write():
    st.title("Decrypt a message using a symmetric encryption algorithm:")

    st.text("The decryption algorithm uses the latest encryption key by default. \n"
            "Please provide us with the key you would like to use")
    st.text("Please provide the secret key: ")
    pwd = st.text_input("Enter a password", type="password")
    cipher_text = st.text_input("Enter your cipher text here")
    if st.button("Get algorithm:"):
        algorithm = get_algorithm(cipher_text)
        st.text(algorithm)
    if st.button("Decrypt:"):
        decrypted, info = decrypt(password=pwd, cipher_text_encoded=cipher_text)
        if decrypted:
            st.text("Succesfully decrypted! The message contained is the following:")
        st.text(info)

