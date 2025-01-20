import pandas as pd

# Colunas esperadas na base
REQUIRED_COLUMNS = [
    "ID SOLICITAÇÃO", "CLIENTE", "DATA SOLICITAÇÃO", "SOLICITANTE", "EQUIPAMENTO", 
    "QUANT EQUIP", "MÓDULO", "QUANT PRANCHAS", "QUANT EIXOS", "TIPO SOLICITAÇÃO",
    "DATA MOVIMENTAÇÃO", "HORA MOVIMENTAÇÃO", "ORIGEM", "DESTINO", "OBS",
    "JUSTIFICATIVA EMERGENCIAL", "TIPO MOVIMENTAÇÃO", "Município Origem",
    "Município Destino", "Aderência Solicitação", "Horas Antecedência", "Ponto A",
    "Origem Ponto B", "Destino Ponto C", "A/B", "B/C", "C/A", "Distância (A/B) (Km)",
    "Distância (B/C) (Km)", "Distância (C/A) (Km)", "KM total", "Horas Deslocamento",
    "Horas Adicionais", "Horas Total", "Movimentações", "Número de Máquinas",
    "Quantidade de Pranchas", "Fornecedor", "Frota 1", "Frota 2", "Frota 3", 
    "Frota 4", "Frota 5", "Frota 6", "Motorista 1", "Motorista 2", "Motorista 3", 
    "Motorista 4", "Motorista 5", "Motorista 6", "Km Ponderada"
]

def load_excel(file):
    try:
        # Carregar o arquivo Excel
        df = pd.read_excel(file)

        # Verificar se todas as colunas obrigatórias estão presentes
        missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_columns:
            raise ValueError(f"As seguintes colunas estão ausentes na base: {', '.join(missing_columns)}")
        
        # Certificar que "DATA MOVIMENTAÇÃO" é tratada como datetime
        df["DATA MOVIMENTAÇÃO"] = pd.to_datetime(df["DATA MOVIMENTAÇÃO"], errors="coerce", dayfirst=True)

        # Certificar que "QUANT EQUIP" é tratada como número
        df["QUANT EQUIP"] = pd.to_numeric(df["QUANT EQUIP"], errors="coerce")

        return df
    except Exception as e:
        print(f"Erro ao carregar o arquivo Excel: {e}")
        return None