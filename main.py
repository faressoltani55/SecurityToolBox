import streamlit as st

import utils.display as udisp

import src.pages.home
import src.pages.hashing
import src.pages.cracking
import src.pages.encoding
import src.pages.symmetric_encryption
import src.pages.symmetric_decryption
import src.pages.asymmetric_encryption
import src.pages.asymmetric_decryption

MENU = {
    "Home": src.pages.home,
    "Coding / Decoding a message": src.pages.encoding,
    "Hashing a message": src.pages.hashing,
    "Cracking a hash": src.pages.cracking,
    "Symmetric Encryption": src.pages.symmetric_encryption,
    "Symmetric Decryption": src.pages.symmetric_decryption,
    "Asymmetric Encryption / Signing" : src.pages.asymmetric_encryption,
    "Asymmetric Decryption / Verifying" : src.pages.asymmetric_decryption
}

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

def main():

    local_css("style.css")
    st.sidebar.title("Navigate yourself...")
    menu_selection = st.sidebar.radio("Chose your option...", list(MENU.keys()))

    menu = MENU[menu_selection]

    with st.spinner(f"Loading {menu_selection} ..."):
        udisp.render_page(menu)


if __name__ == '__main__':
    main()

