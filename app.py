import streamlit as st

import awesome_streamlit as ast
import src.pages.logins_per_day
import src.pages.articles
import src.pages.home

ast.core.services.other.set_logging_format()

PAGES = {
    "Home": src.pages.home,
    "Anmeldungen": src.pages.logins_per_day,
    "Artikel": src.pages.articles
}

def main():
    """Main function of the App"""
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        ast.shared.components.write_page(page)


if __name__ == "__main__":
    main()