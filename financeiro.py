import streamlit as st
import pandas as pd
import json
from github import Github
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# Configuração do GitHub
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "Scsant/dadosPrancha"
FINANCE_FILE_PATH = "financeiroTransporte.json"

# Função para carregar dados financeiros do GitHub
def load_finance_data():
    st.write("Carregando dados financeiros do GitHub...")
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    file = repo.get_contents(FINANCE_FILE_PATH)
    content = file.decoded_content.decode("utf-8")

    try:
        data = json.loads(content)
        if isinstance(data, list):
            return pd.DataFrame(data)
        else:
            st.error("Erro: O arquivo JSON não contém uma lista de registros válidos.")
            return pd.DataFrame()
    except json.JSONDecodeError:
        st.error("Erro ao decodificar JSON do GitHub.")
        return pd.DataFrame()

# Função para gerar recibo em PDF
def gerar_recibo(df_financeiro, id_solicitacao):
    st.write("Gerando recibo...")

    df_filtrado = df_financeiro[df_financeiro["CTE/NF"] == id_solicitacao]

    if df_filtrado.empty:
        st.error("Nenhum registro encontrado para o ID fornecido.")
        return None

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Recibo de Transporte", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"ID Solicitação: {id_solicitacao}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", size=10)
    for index, row in df_filtrado.iterrows():
        for col in df_filtrado.columns:
            pdf.cell(90, 10, f"{col}:", border=1)
            pdf.cell(90, 10, f"R$ {row[col]:,.2f}", border=1, ln=True)

    pdf.ln(10)
    pdf.cell(0, 10, "Assinatura: ___________________________", ln=True)

    recibo_path = f"recibo_{id_solicitacao}.pdf"
    pdf.output(recibo_path)

    st.success("Recibo gerado com sucesso!")
    return recibo_path

# Função para enviar e-mail com recibo
def enviar_email(recibo_path, destinatario):
    remetente = os.getenv("EMAIL_USER")
    senha = os.getenv("EMAIL_PASS")

    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = "Recibo de Transporte"

    with open(recibo_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={recibo_path}")
        msg.attach(part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(remetente, senha)
        server.sendmail(remetente, destinatario, msg.as_string())
        server.quit()
        st.success("E-mail enviado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao enviar e-mail: {e}")

# Interface Streamlit
def display_financeiro():
    st.title("Gestão Financeira de Transporte")

    df_financeiro = load_finance_data()

    if df_financeiro.empty:
        st.warning("Nenhuma informação financeira encontrada.")
    else:
        tab1, tab2, tab3 = st.tabs(["Consulta Financeira", "Gerar Recibo", "Enviar E-mail"])

        with tab1:
            st.subheader("Registros Financeiros Salvos")
            st.dataframe(df_financeiro)

        with tab2:
            id_solicitacao = st.selectbox("Selecione o ID da Solicitação:", df_financeiro["CTE/NF"].unique())

            if st.button("Gerar Recibo PDF"):
                recibo_path = gerar_recibo(df_financeiro, id_solicitacao)
                if recibo_path:
                    with open(recibo_path, "rb") as file:
                        st.download_button(label="Baixar Recibo", data=file, file_name=recibo_path, mime="application/pdf")

        with tab3:
            email_destinatario = st.text_input("Digite o e-mail para envio:")
            if st.button("Enviar Recibo por E-mail"):
                if email_destinatario and recibo_path:
                    enviar_email(recibo_path, email_destinatario)
                else:
                    st.warning("Por favor, gere o recibo primeiro e insira um e-mail válido.")

if __name__ == "__main__":
    display_financeiro()
import streamlit as st
import pandas as pd
import json
from github import Github
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# Configuração do GitHub
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "Scsant/dadosPrancha"
FINANCE_FILE_PATH = "financeiroTransporte.json"

# Função para carregar dados financeiros do GitHub
def load_finance_data():
    st.write("Carregando dados financeiros do GitHub...")
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    file = repo.get_contents(FINANCE_FILE_PATH)
    content = file.decoded_content.decode("utf-8")

    try:
        data = json.loads(content)
        if isinstance(data, list):
            return pd.DataFrame(data)
        else:
            st.error("Erro: O arquivo JSON não contém uma lista de registros válidos.")
            return pd.DataFrame()
    except json.JSONDecodeError:
        st.error("Erro ao decodificar JSON do GitHub.")
        return pd.DataFrame()

# Função para gerar recibo em PDF
def gerar_recibo(df_financeiro, id_solicitacao):
    st.write("Gerando recibo...")

    df_filtrado = df_financeiro[df_financeiro["CTE/NF"] == id_solicitacao]

    if df_filtrado.empty:
        st.error("Nenhum registro encontrado para o ID fornecido.")
        return None

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Recibo de Transporte", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"ID Solicitação: {id_solicitacao}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", size=10)
    for index, row in df_filtrado.iterrows():
        for col in df_filtrado.columns:
            pdf.cell(90, 10, f"{col}:", border=1)
            try:
                valor = float(row[col])  # Converte para float se possível
                pdf.cell(90, 10, f"R$ {valor:,.2f}", border=1, ln=True)
            except ValueError:
                pdf.cell(90, 10, f"{col}: {row[col]}", border=1, ln=True)  # Mantém como texto se não for número


    pdf.ln(10)
    pdf.cell(0, 10, "Assinatura: ___________________________", ln=True)

    recibo_path = f"recibo_{id_solicitacao}.pdf"
    pdf.output(recibo_path)

    st.success("Recibo gerado com sucesso!")
    return recibo_path

# Função para enviar e-mail com recibo
def enviar_email(recibo_path, destinatario):
    remetente = os.getenv("EMAIL_USER")
    senha = os.getenv("EMAIL_PASS")

    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = "Recibo de Transporte"

    with open(recibo_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={recibo_path}")
        msg.attach(part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(remetente, senha)
        server.sendmail(remetente, destinatario, msg.as_string())
        server.quit()
        st.success("E-mail enviado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao enviar e-mail: {e}")

# Interface Streamlit
def display_financeiro():
    st.title("Gestão Financeira de Transporte")

    df_financeiro = load_finance_data()

    if df_financeiro.empty:
        st.warning("Nenhuma informação financeira encontrada.")
    else:
        tab1, tab2, tab3 = st.tabs(["Consulta Financeira", "Gerar Recibo", "Enviar E-mail"])

        with tab1:
            st.subheader("Registros Financeiros Salvos")
            st.dataframe(df_financeiro)

        with tab2:
            id_solicitacao = st.selectbox("Selecione o ID da Solicitação:", df_financeiro["CTE/NF"].unique())

            if st.button("Gerar Recibo PDF"):
                recibo_path = gerar_recibo(df_financeiro, id_solicitacao)
                if recibo_path:
                    with open(recibo_path, "rb") as file:
                        st.download_button(label="Baixar Recibo", data=file, file_name=recibo_path, mime="application/pdf")

        with tab3:
            email_destinatario = st.text_input("Digite o e-mail para envio:")
            if st.button("Enviar Recibo por E-mail"):
                if email_destinatario and recibo_path:
                    enviar_email(recibo_path, email_destinatario)
                else:
                    st.warning("Por favor, gere o recibo primeiro e insira um e-mail válido.")

if __name__ == "__main__":
    display_financeiro()
