from github import Github
import json

def save_to_github(token, repo_name, file_path, new_data):
    try:
        print("Iniciando conexão com o GitHub...")  # Log inicial
        g = Github(token)
        repo = g.get_repo(repo_name)

        print("Obtendo conteúdo do arquivo...")  # Verifica se o arquivo existe
        file = repo.get_contents(file_path)
        content = file.decoded_content.decode("utf-8")
        print("Conteúdo atual do arquivo:", content)

        # Atualizar o conteúdo com os novos dados
        existing_data = json.loads(content) if content else []
        print("Dados existentes no arquivo:", existing_data)

        if isinstance(existing_data, list):
            existing_data.append(new_data)
        else:
            raise ValueError("O arquivo JSON no repositório não contém uma lista.")

        updated_content = json.dumps(existing_data, indent=4)
        print("Conteúdo atualizado:", updated_content)

        # Atualizar o arquivo no GitHub
        repo.update_file(
            path=file_path,
            message="Atualização: Nova programação adicionada",
            content=updated_content,
            sha=file.sha
        )
        print("Arquivo atualizado com sucesso no GitHub.")
    except Exception as e:
        print(f"Erro na função save_to_github: {e}")
