import streamlit as st

from src.logic.symmetric.constants import SYM_ALGORITHMS
from src.logic.symmetric.functions import generate_secret_key, get_key_sizes, download_secret_key, encrypt, \
    reset_key, algorithm_strength


def write():

    reset_key()
    
    st.title("Encrypt a message using a symmetric encryption algorithm:")

    message = st.text_input("Enter your message here")

    algorithm = st.selectbox("Choose the symmetric encryption algorithm:", SYM_ALGORITHMS)
    if algorithm_strength(algorithm) == 0:
        st.error('This algorithm is not secure! Please keep that in mind.')
    key_size = st.selectbox("Choose the size of the key to be generated:", get_key_sizes(algorithm))
    st.text("Please enter a password to generate the key: ")
    pwd = st.text_input("Enter a password", type="password")


    if st.button("Generate Key & Encrypt"):

        key = generate_secret_key(key_size, pwd)
        st.success("Secret key generated successfully!")
        st.markdown(download_secret_key(key), unsafe_allow_html=True)

        cipher_text = encrypt(algorithm, key, message)
        st.success("Message Encrypted Successfully!")
        st.text(cipher_text)

