from github import Github
import json

# Exemplo de teste
GITHUB_TOKEN = "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"
REPO_NAME = "Scsant/dadosPrancha"
FILE_PATH = "programacaoRealizada.json"

# Dados para testar
new_data = {
    "ID Solicitação": 123,
    "Supervisor": "João Silva",
    "Placa Cavalo": "ABC1234",
    "Motorista": "Carlos Souza",
    "Tipo de Transporte": "Próprio",
    "Prancha": "Placa: GPC1321 - Tipo: 3 EIXOS SIMPLES",
    "Máquina": "Escavadeira",
    "Viagem": 1,
}

def save_to_github_test():
    try:
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
            raise ValueError("O arquivo JSON no repositório não contém uma lista.")

        # Serializar os dados atualizados
        updated_content = json.dumps(existing_data, indent=4)

        # Atualizar o arquivo no repositório
        repo.update_file(
            path=FILE_PATH,
            message="Teste: Adicionando nova programação",
            content=updated_content,
            sha=file.sha
        )
        print("Arquivo atualizado com sucesso no GitHub.")
    except Exception as e:
        print(f"Erro ao salvar no GitHub: {e}")

save_to_github_test()
