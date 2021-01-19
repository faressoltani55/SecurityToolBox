import streamlit as st

from src.logic.symmetric.functions import get_algorithm, decrypt


def write():
    st.title("Decrypt a message using a symmetric encryption algorithm:")
    cipher_text = st.text_input("Enter your cipher text here")

    if st.button("Get algorithm:"):
        algorithm = get_algorithm(cipher_text)
        st.text(algorithm)

    pwd = st.text_input("Enter the password", type="password")

    if st.button("Decrypt:"):
        decrypted, info = decrypt(password=pwd, cipher_text_encoded=cipher_text)
        if decrypted:
            st.text("Successfully decrypted! The message is the following:")
        st.text(info)
