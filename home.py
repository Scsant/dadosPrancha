import streamlit as st
from utils.file_handler import load_excel

def display_home():
    st.title("Página Inicial")
    st.write("Carregue a base de dados para começar.")

    # Verificar se a base já está carregada no session_state
    if "data" not in st.session_state:
        st.session_state["data"] = None

    # Exibir mensagem caso a base já esteja carregada
    if st.session_state["data"] is not None:
        st.success("A base de dados já foi carregada.")
        st.dataframe(st.session_state["data"])
        return

    # Botão para carregar nova base
    uploaded_file = st.file_uploader("Carregar Base de Dados", type=["xlsx"])
    
    if uploaded_file is not None:
        df = load_excel(uploaded_file)
        
        if df is not None:
            st.success("Base de dados carregada com sucesso!")

            # Salvar a base no session state
            st.session_state["data"] = df

            # Exibir DataFrame
            st.dataframe(df)
        else:
            st.error("Erro ao carregar a base de dados. Verifique se o arquivo está no formato correto.")
