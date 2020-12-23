# Import the hashlib library :
import hashlib as hl
import streamlit as st


# Show available hash functions :
def hash_algorithms():
    return sorted(list(filter(lambda v: "_" not in v, hl.algorithms_guaranteed)))


# Algorithms :
def blake2b(word):
    return hl.blake2b(word.encode('UTF-8')).hexdigest()


def blake2s(word):
    return hl.blake2s(word.encode('UTF-8')).hexdigest()


def md5(word):
    return hl.md5(word.encode('UTF-8')).hexdigest()


def sha1(word):
    return hl.sha1(word.encode('UTF-8')).hexdigest()


def sha224(word):
    return hl.sha224(word.encode('UTF-8')).hexdigest()


def sha256(word):
    return hl.sha256(word.encode('UTF-8')).hexdigest()


def sha384(word):
    return hl.sha384(word.encode('UTF-8')).hexdigest()


def sha512(word):
    return hl.sha512(word.encode('UTF-8')).hexdigest()


def write():
    st.title("Here, you can chose a hashing algorithm and calculate the hash of a word")
    choice = st.selectbox("Choose the algorithm :", hash_algorithms())
    word = st.text_input("Enter your word here", "Type here ...")
    if st.button("Calculate"):
        if choice == "blake2b":
            st.info(blake2b(word))
        elif choice == "blake2s":
            st.info(blake2s(word))
        elif choice == "md5":
            st.info(md5(word))
        elif choice == "sha1":
            st.info(sha1(word))
        elif choice == "sha224":
            st.info(sha224(word))
        elif choice == "sha256":
            st.info(sha256(word))
        elif choice == "sha384":
            st.info(sha384(word))
        elif choice == "sha512":
            st.info(sha512(word))