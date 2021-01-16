import streamlit as st

import utils.display as udisp

import src.pages.home
import src.pages.hashing
import src.pages.cracking
import src.pages.asymmetric_encryption
import src.pages.asymmetric_decryption

MENU = {
    "Home": src.pages.home,
    # "Coding / Decoding a Message": src.pages.coding,
    "Hashing a message": src.pages.hashing,
    "Cracking a hash": src.pages.cracking,
    "Asymmetric Encryption / Signing" : src.pages.asymmetric_encryption,
    "Asymmetric Decryption / Verifying" : src.pages.asymmetric_decryption
}


def main():
    st.sidebar.title("Navigate yourself...")
    menu_selection = st.sidebar.radio("Chose your option...", list(MENU.keys()))

    menu = MENU[menu_selection]

    with st.spinner(f"Loading {menu_selection} ..."):
        udisp.render_page(menu)


if __name__ == '__main__':
    main()

