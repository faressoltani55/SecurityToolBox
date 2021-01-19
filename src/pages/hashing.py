# Import the hashlib library :
import streamlit as st

from src.logic.hash.functions import calc_hash, hash_algorithms


def write():
    st.title("Here, you can chose a hashing algorithm and calculate the hash of a word")
    choice = st.selectbox("Choose the algorithm :", hash_algorithms())
    word = st.text_input("Enter your word here")
    if st.button("Calculate Hash"):
        st.text(calc_hash(choice,word))