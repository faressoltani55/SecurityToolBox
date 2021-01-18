import utils.symmetric.algorithms as sym_utils
import streamlit as st

from src.logic.symmetric.functions import get_algorithm, decrypt


def write():
    st.title("Decrypt a message using a symmetric encryption algorithm:")
    cipher_text = st.text_input("Enter your cipher text here")

    if st.button("Get algorithm:"):
        algorithm = get_algorithm(cipher_text)
        st.text(algorithm)

#   st.text("Please provide us with the key in case you weren't the user who generated it: ")
#    uploaded_file = st.file_uploader("Choose the key file")
#    upload_secret_key(uploaded_file)
    pwd = st.text_input("Enter the password", type="password")

    if st.button("Decrypt:"):
        decrypted, info = decrypt(password=pwd, cipher_text_encoded=cipher_text)
        if decrypted:
            st.text("Successfully decrypted! The message contained is the following:")
        st.text(info)

