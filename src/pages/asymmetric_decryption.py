import streamlit as st
from cryptography.exceptions import InvalidSignature

from src.logic.asymmetric.functions import verify, get_algorithm, decrypt


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
