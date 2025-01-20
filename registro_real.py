import streamlit as st
import pandas as pd
import json
from github import Github

# Configuração do GitHub
GITHUB_TOKEN = "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"
REPO_NAME = "Scsant/dadosPrancha"
FILE_PATH = "programacaoRealizada.json"

# Função para carregar os dados do GitHub
@st.cache_data(ttl=600)
def load_data_from_github():
    st.write("Carregando dados do GitHub...")
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    file = repo.get_contents(FILE_PATH)
    content = file.decoded_content.decode("utf-8")

    try:
        data = json.loads(content)
        
        # Converter listas aninhadas em uma única lista de dicionários
        flattened_data = []
        for item in data:
            if isinstance(item, list):  # Se for uma lista, extrai os elementos
                flattened_data.extend(item)
            else:
                flattened_data.append(item)

        if all(isinstance(item, dict) for item in flattened_data):
            return pd.DataFrame(flattened_data)
        else:
            st.error("Erro: O arquivo JSON contém dados inconsistentes.")
            return pd.DataFrame()
    except json.JSONDecodeError:
        st.error("Erro ao decodificar JSON do GitHub.")
        return pd.DataFrame()

def display_registro_transporte():
    st.title("Registro de Transporte Realizado")
    st.write("Bem-vindo à página de Registro de Transporte!")

    df_programacao = load_data_from_github()

    if df_programacao.empty:
        st.warning("Nenhum dado encontrado no GitHub.")
        return

    st.subheader("Programação Salva no GitHub")
    st.dataframe(df_programacao)

    # Filtrar por ID Solicitação
    id_selecionado = st.selectbox("Selecione o ID da Solicitação:", df_programacao["ID Solicitação"].unique())

    # Filtrar os dados pelo ID selecionado
    df_filtrado = df_programacao[df_programacao["ID Solicitação"] == id_selecionado]
    st.subheader(f"Registro de Transporte para ID: {id_selecionado}")
    st.dataframe(df_filtrado)

    # Formulário para preenchimento dos dados reais
    st.subheader("Preencher Transporte Realizado")

    centro_maquina = st.text_input("Centro Máquina")
    descricao_maquina = st.text_input("Descrição Máquina")
    municipio_origem = st.text_input("Município Origem")
    municipio_destino = st.text_input("Município Destino")
    nota_fiscal = st.text_input("Nota Fiscal Transferência")
    carta_correcao = st.text_input("Carta Correção")
    km_inicial = st.number_input("KM Inicial", min_value=0)
    km_final = st.number_input("KM Final", min_value=0)
    km_total = km_final - km_inicial
    hora_inicio = st.time_input("Hora Início")
    chegada_fazenda = st.time_input("Chegada na Fazenda")
    embarque = st.time_input("Embarque")
    desembarque = st.time_input("Desembarque")
    saida_fazenda = st.time_input("Saída Fazenda")
    hora_fim = st.time_input("Hora Fim")
    hora_total = st.time_input("Hora Total")
    observacao = st.text_area("Observação")

    # Botão para salvar os dados preenchidos
    if st.button("Salvar Transporte Realizado"):
        new_data = {
            "ID Solicitação": id_selecionado,
            "Centro Máquina": centro_maquina,
            "Descrição Máquina": descricao_maquina,
            "Município Origem": municipio_origem,
            "Município Destino": municipio_destino,
            "Nota Fiscal Transferência": nota_fiscal,
            "Carta Correção": carta_correcao,
            "KM Inicial": km_inicial,
            "KM Final": km_final,
            "KM Total": km_total,
            "Hora Início": str(hora_inicio),
            "Chegada na Fazenda": str(chegada_fazenda),
            "Embarque": str(embarque),
            "Desembarque": str(desembarque),
            "Saída Fazenda": str(saida_fazenda),
            "Hora Fim": str(hora_fim),
            "Hora Total": str(hora_total),
            "Observação": observacao
        }

        # Concatenar com os dados originais
        df_concatenado = pd.concat([df_filtrado, pd.DataFrame([new_data])], ignore_index=True)

        # Mostrar os dados antes de salvar
        st.subheader("Dados atualizados antes de salvar")
        st.dataframe(df_concatenado)

        # Salvar no GitHub após confirmação do usuário
        if st.button("Enviar para GitHub"):
            save_to_github(df_concatenado.to_dict(orient="records"))

def save_to_github(data):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    try:
        file = repo.get_contents(FILE_PATH)
        content = file.decoded_content.decode("utf-8")
        existing_data = json.loads(content) if content else []
        file_sha = file.sha  # Para atualização do arquivo existente
    except:
        existing_data = []
        file_sha = None

    updated_data = existing_data + data
    updated_content = json.dumps(updated_data, indent=4)

    if file_sha:
        repo.update_file(FILE_PATH, "Atualização: Transporte Realizado", updated_content, file_sha)
    else:
        repo.create_file(FILE_PATH, "Criação: Transporte Realizado", updated_content)

    st.success("Dados de transporte real salvos com sucesso!")
