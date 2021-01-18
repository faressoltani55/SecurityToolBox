import utils.symmetric.algorithms as sym_utils
import streamlit as st

from src.logic.symmetric.functions import generate_secret_key, get_key_sizes, get_key, encrypt


def write():
    st.title("Encrypt a message using a symmetric encryption algorithm:")
    algorithm = st.selectbox("Choose the symmetric encryption algorithm:", sym_utils.SYM_ALGORITHMS)
    key_size = st.selectbox("Choose the size of the key to be generated:", get_key_sizes(algorithm))
    st.text("Please enter a password to generate the key: ")
    pwd = st.text_input("Enter a password", type="password")

    if st.button("Generate Secret Key"):
        key = generate_secret_key(key_size, pwd)
        st.success("Secret key generated successfully!")

    message = st.text_input("Enter your message here")

    if st.button("Encrypt"):
        key = get_key()
        if key is None:
            st.warning("Please generate a secret key first!")
        else:
            cipher_text = encrypt(algorithm, get_key(), message)
            st.success("Message Encrypted Successfully!")
            st.text(cipher_text)
