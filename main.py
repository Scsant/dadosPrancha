import streamlit as st
from pages import home, programacao, registro_real, financeiro

st.set_page_config(page_title="Gerenciamento de Transporte", layout="wide")

def main():
    st.sidebar.title("Menu")
    menu = st.sidebar.radio("Navegar", ["Página Inicial", "Painel de Programação", "Registro de Transporte", "Financeiro"])

    if menu == "Página Inicial":
        home.display_home()
    elif menu == "Painel de Programação":
        programacao.display_programacao()
    elif menu == "Registro de Transporte":
        registro_real.display_registro_transporte()
    elif menu == "Financeiro":
        financeiro.display_financeiro()

if __name__ == "__main__":
    main()
