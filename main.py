import streamlit as st

import utils.display as udisp

import src.pages.home
import src.pages.hashing
import src.pages.cracking
import src.pages.encoding
import src.pages.symmetric_encryption
import src.pages.symmetric_decryption
import src.pages.asymmetric_decryption
import src.pages.asymmetric_decryption

MENU = {
    "Home": src.pages.home,
    "Coding / Decoding a message": src.pages.encoding,
    "Hashing a message": src.pages.hashing,
    "Cracking a hash": src.pages.cracking,
    "Symmetric Encryption": src.pages.symmetric_encryption,
    "Symmetric Decryption": src.pages.symmetric_decryption,
    "Asymmetric Encryption / Signing" : src.pages.asymmetric_decryption,
    "Asymmetric Decryption / Verifying" : src.pages.asymmetric_decryption
}


def main():
    st.markdown(
        """
        <style>
        .reportview-container {
            background-color: black;
            color: lime
        }
       .css-1aumxhk {
            background-color: #011839;
            background-image: none;
            color: lime
        }
        .st-bw {
            color: lime
        }
        .css-145kmo2 {
            color: white
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.title("Navigate yourself...")
    menu_selection = st.sidebar.radio("Chose your option...", list(MENU.keys()))

    menu = MENU[menu_selection]

    with st.spinner(f"Loading {menu_selection} ..."):
        udisp.render_page(menu)


if __name__ == '__main__':
    main()

