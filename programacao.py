import streamlit as st
import pandas as pd
import requests
import json
from github import Github
# Garantir que a chave "pagina_atual" esteja definida
if "pagina_atual" not in st.session_state:
    st.session_state["pagina_atual"] = "Página Inicial"

# Adicione seu token pessoal do GitHub aqui (certifique-se de mantê-lo seguro!)
GITHUB_TOKEN = "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"
REPO_NAME = "Scsant/dadosPrancha"
FILE_PATH = "programacaoRealizada.json"

# Inicializar session_state para armazenar dados carregados
if "data" not in st.session_state:
    st.session_state["data"] = None

if "programacoes" not in st.session_state:
    st.session_state["programacoes"] = []
    
# Função para carregar dados das APIs e transportadora.json
def load_api_data():
    if "data_sources" not in st.session_state:
        st.session_state["data_sources"] = {}

    try:
        # Caminhões Próprios
        response_cm = requests.get("https://solicitacoes.onrender.com/api/cm/")
        st.session_state["data_sources"]["caminhoes"] = response_cm.json()

        # Carretas Pranchas
        response_pranchas = requests.get("https://solicitacoes.onrender.com/api/pranchas/")
        st.session_state["data_sources"]["pranchas"] = response_pranchas.json()

        # Motoristas - Turno Dia
        response_motoristas_dia = requests.get("https://solicitacoes.onrender.com/api/escala-dia/")
        st.session_state["data_sources"]["motoristas_dia"] = response_motoristas_dia.json()

        # Transportadora (arquivo JSON local)
        with open("transportadora.json", "r") as file:
            st.session_state["data_sources"]["transportadoras"] = json.load(file)

        st.success("Dados das APIs carregados com sucesso!")
    except Exception as e:
        st.error(f"Erro ao carregar dados das APIs ou arquivo JSON: {e}")
    
    

# Função para salvar dados no GitHub
def save_to_github(new_data):
    try:
        st.write("Iniciando conexão com GitHub...")

        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)

        # Obter o conteúdo atual do arquivo
        file = repo.get_contents(FILE_PATH)
        content = file.decoded_content.decode("utf-8")
        existing_data = json.loads(content) if content else []

        # Adicionar os novos dados
        if isinstance(existing_data, list):
            existing_data.append(new_data)
        else:
            raise ValueError("O arquivo JSON no repositório não contém uma lista válida.")

        # Serializar os dados atualizados
        updated_content = json.dumps(existing_data, indent=4)

        # Atualizar o arquivo no repositório
        repo.update_file(
            path=FILE_PATH,
            message="Atualização: Adicionando nova programação",
            content=updated_content,
            sha=file.sha
        )

        st.success("Arquivo atualizado com sucesso no GitHub.")
    except Exception as e:
        st.error(f"Erro ao salvar no GitHub: {e}")
        print(f"Erro ao salvar no GitHub: {e}")


# Função para exibir a página de programação
def display_programacao():
    st.title("Painel de Programação")
    st.write("Filtre os dados, selecione uma solicitação e adicione a programação.")

    if st.session_state["data"] is None:
        st.error("Base de dados não carregada. Por favor, volte à Página Inicial para carregar a base.")
        if st.button("Voltar para Carregar Base"):
            st.session_state["pagina_atual"] = "carregar_base"
        return

    # Inicializa session_state["data_sources"] se ainda não estiver inicializado
    if "data_sources" not in st.session_state:
        st.session_state["data_sources"] = {}

    # Carregar dados das APIs se ainda não estiverem carregados
    if "caminhoes" not in st.session_state["data_sources"]:
        load_api_data()


    df = st.session_state["data"]

    # Filtro por "DATA MOVIMENTAÇÃO"
    st.subheader("Filtro por Data de Movimentação")
    datas_disponiveis = pd.to_datetime(df["DATA MOVIMENTAÇÃO"]).dt.date.unique()
    data_selecionada = st.selectbox("Selecione a Data de Movimentação:", datas_disponiveis)

    # Exibir painel de métricas logo abaixo da escolha da data
    if data_selecionada:
        df_filtrado = df[pd.to_datetime(df["DATA MOVIMENTAÇÃO"]).dt.date == data_selecionada]

        st.subheader(f"Informações da Data {data_selecionada}")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Total de Solicitações", value=df_filtrado["ID SOLICITAÇÃO"].nunique())
        with col2:
            st.metric(label="Total de Máquinas a Transportar", value=df_filtrado["QUANT EQUIP"].sum())

        # Exibir tabela de solicitações
        st.subheader(f"Solicitações para {data_selecionada}")
        st.dataframe(df_filtrado)

        # Seleção de ID da solicitação com lista suspensa
        id_selecionado = st.selectbox("Selecione o ID da Solicitação:", df_filtrado["ID SOLICITAÇÃO"].unique())

        detalhes = df_filtrado[df_filtrado["ID SOLICITAÇÃO"] == id_selecionado]
        st.write("**Detalhes da Solicitação Selecionada:**")
        st.dataframe(detalhes)

        quant_equip = int(detalhes["QUANT EQUIP"].iloc[0])

        st.subheader("Adicionar Programação")
        tipo_transporte = st.radio("Selecione o Tipo de Transporte:", ["Próprio", "Terceirizado"])

        for viagem in range(quant_equip):
            st.write(f"**Programação para Viagem {viagem + 1}**")

            with st.form(key=f"form_programacao_{viagem}"):
                supervisor = st.text_input("Supervisor/Responsável", key=f"supervisor_{viagem}")
                maquina = st.selectbox("Máquina", detalhes["EQUIPAMENTO"].unique(), key=f"maquina_{viagem}")

                if tipo_transporte == "Próprio":
                    placas_caminhoes = [f"BTF: {item['btf']}" for item in st.session_state["data_sources"]["caminhoes"]]
                    placa_cavalo = st.selectbox("Placa Cavalo", placas_caminhoes, key=f"placa_cavalo_{viagem}")

                    motoristas = [f"{item['colaborador']} - Matricula: {item['matricula']}" 
                                  for item in st.session_state["data_sources"]["motoristas_dia"]]
                    motorista = st.selectbox("Motorista", motoristas, key=f"motorista_{viagem}")

                    pranchas = [f"{item['placa']} - {item['tipo']}" 
                                for item in st.session_state["data_sources"]["pranchas"]]
                    prancha = st.selectbox("Prancha", pranchas, key=f"prancha_{viagem}")

                else:
                    transportadoras = [item["NOME"] for item in st.session_state["data_sources"]["transportadoras"]]
                    fornecedor = st.selectbox("Fornecedor", transportadoras, key=f"fornecedor_{viagem}")

                    placa_cavalo = st.text_input("Placa Cavalo", key=f"placa_terc_{viagem}")
                    motorista = st.text_input("Motorista", key=f"motorista_terc_{viagem}")
                    prancha = "N/A"

                submit_button = st.form_submit_button(label="Salvar Programação")


                if submit_button:
                    st.session_state["programacoes"].append({
                        "ID Solicitação": id_selecionado,
                        "Supervisor": supervisor,
                        "Placa Cavalo": placa_cavalo,
                        "Motorista": motorista,
                        "Tipo de Transporte": tipo_transporte,
                        "Fornecedor": fornecedor if tipo_transporte == "Terceirizado" else None,
                        "Prancha": prancha,
                        "Máquina": maquina,
                        "Viagem": viagem + 1,
                    })
                    st.success(f"Programação para Viagem {viagem + 1} adicionada com sucesso!")


    # Exibir programações salvas após a criação dos formulários
    if "programacoes" in st.session_state and len(st.session_state["programacoes"]) > 0:
        st.subheader("Programações Criadas")
        st.dataframe(pd.DataFrame(st.session_state["programacoes"]))
        
    # Botão para salvar no GitHub
    if st.button("Enviar para GitHub"):
        if st.session_state["programacoes"]:
            st.write("Enviando os dados para o GitHub...")
            save_to_github(st.session_state["programacoes"])
            st.success("Programação enviada ao GitHub com sucesso!")
        else:
            st.warning("Nenhuma programação para enviar.")

    if st.button("Voltar para Carregar Base"):
        st.session_state["pagina_atual"] = "carregar_base"


if st.session_state["pagina_atual"] == "programacao":
    display_programacao()
