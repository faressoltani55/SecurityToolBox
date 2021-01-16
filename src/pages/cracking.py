# Import the hashlib library :
import hashlib as hl
import streamlit as st
from src.pages.hashing import calc_hash
import os


def hash_algorithms():
    return sorted(list(filter(lambda v: "_" not in v, hl.algorithms_guaranteed)))


def write():
    st.title("Here, you can crack a hash to retrieve the hidden word")
    algo = st.selectbox("Choose the algorithm :", hash_algorithms())
    dictionary = st.selectbox("Choose the Dictionary :", ["Small", "Medium", "Big", "Giant"])
    script_dir = os.path.dirname(__file__)
    rel_path = "../../utils/dictionaries/"+dictionary+".txt"
    path = os.path.join(script_dir, rel_path)
    wordlist = open(path, 'r').readlines()
    hash_a = st.text_input("Enter your hash here")
    success = False
    if st.button("Crack !"):
        for word in wordlist:
            word = word.strip()
            hash_b = calc_hash(algo, word)
            if hash_a == hash_b:
                success = True
                st.success("Word Cracked : "+word)
                break
        if not success:
            st.error("Word is hard to crack, try changing the dictionary and make sure you picked the right hashing algorithm")