import requests
import json

# URL base da nossa API
BASE_URL = "http://127.0.0.1:5000/tasks"

# --- Funções CRUD (mantidas como estão no seu código original) ---
def get_all_tasks():
    """Busca e exibe todas as tarefas."""
    print("\n--- Listando todas as tarefas ---")
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        tasks = response.json()
        if tasks:
            for task in tasks:
                print(f"ID: {task['id']}, Título: {task['title']}, Status: {task['status']}")
        else:
            print("Nenhuma tarefa encontrada.")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar tarefas: {e}")

def get_task_by_id(task_id):
    """Busca e exibe uma tarefa específica pelo ID."""
    print(f"\n--- Buscando tarefa com ID: {task_id} ---")
    try:
        response = requests.get(f"{BASE_URL}/{task_id}")
        response.raise_for_status()
        task = response.json()
        print(f"ID: {task['id']}, Título: {task['title']}, Descrição: {task['description']}, Status: {task['status']}")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Tarefa com ID {task_id} não encontrada.")
        else:
            print(f"Erro HTTP ao buscar tarefa: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao buscar tarefa: {e}")

def create_task(title, description="", status="pendente"):
    """Cria uma nova tarefa."""
    print(f"\n--- Criando tarefa: '{title}' ---")
    task_data = {
        "title": title,
        "description": description,
        "status": status
    }
    try:
        response = requests.post(BASE_URL, json=task_data)
        response.raise_for_status()
        new_task = response.json()
        print(f"Tarefa criada com sucesso! ID: {new_task['id']}, Título: {new_task['title']}")
        return new_task['id']
    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP ao criar tarefa: {e}")
        print(f"Detalhes: {e.response.json().get('message', 'Nenhum detalhe')}")
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao criar tarefa: {e}")
    return None

def update_task(task_id, title=None, description=None, status=None):
    """Atualiza uma tarefa existente pelo ID."""
    print(f"\n--- Atualizando tarefa com ID: {task_id} ---")
    update_data = {}
    if title is not None:
        update_data['title'] = title
    if description is not None:
        update_data['description'] = description
    if status is not None:
        update_data['status'] = status

    if not update_data:
        print("Nenhum dado para atualização fornecido.")
        return

    try:
        response = requests.put(f"{BASE_URL}/{task_id}", json=update_data)
        response.raise_for_status()
        updated_task = response.json()
        print(f"Tarefa com ID {task_id} atualizada com sucesso!")
        print(f"Novo estado: Título: {updated_task['title']}, Status: {updated_task['status']}")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Tarefa com ID {task_id} não encontrada para atualização.")
        else:
            print(f"Erro HTTP ao atualizar tarefa: {e}")
            print(f"Detalhes: {e.response.json().get('message', 'Nenhum detalhe')}")
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao atualizar tarefa: {e}")

def delete_task(task_id):
    """Deleta uma tarefa específica pelo ID."""
    print(f"\n--- Deletando tarefa com ID: {task_id} ---")
    try:
        response = requests.delete(f"{BASE_URL}/{task_id}")
        response.raise_for_status()
        message = response.json().get('message', 'Tarefa deletada.')
        print(message)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Tarefa com ID {task_id} não encontrada para exclusão.")
        else:
            print(f"Erro HTTP ao deletar tarefa: {e}")
            print(f"Detalhes: {e.response.json().get('message', 'Nenhum detalhe')}")
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao deletar tarefa: {e}")

# --- Menu Interativo para o usuário ---
def main_menu():
    while True:
        print("\n--- Menu de Gerenciamento de Tarefas ---")
        print("1. Listar todas as tarefas")
        print("2. Buscar tarefa por ID")
        print("3. Criar nova tarefa")
        print("4. Atualizar tarefa existente")
        print("5. Deletar tarefa")
        print("6. Sair")

        choice = input("Escolha uma opção: ")

        if choice == '1':
            get_all_tasks()
        elif choice == '2':
            try:
                task_id = int(input("Digite o ID da tarefa para buscar: "))
                get_task_by_id(task_id)
            except ValueError:
                print("ID inválido. Por favor, digite um número.")
        elif choice == '3':
            title = input("Digite o título da nova tarefa: ")
            description = input("Digite a descrição (opcional, deixe em branco para pular): ")
            status = input("Digite o status (opcional, 'pendente', 'em progresso', 'concluida', etc., deixe em branco para 'pendente'): ")
            create_task(title, description if description else "", status if status else "pendente")
        elif choice == '4':
            try:
                task_id = int(input("Digite o ID da tarefa para atualizar: "))
                title = input("Novo título (opcional, deixe em branco para não alterar): ")
                description = input("Nova descrição (opcional, deixe em branco para não alterar): ")
                status = input("Novo status (opcional, deixe em branco para não alterar): ")

                update_task(
                    task_id,
                    title if title else None,
                    description if description else None,
                    status if status else None
                )
            except ValueError:
                print("ID inválido. Por favor, digite um número.")
        elif choice == '5':
            try:
                task_id = int(input("Digite o ID da tarefa para deletar: "))
                delete_task(task_id)
            except ValueError:
                print("ID inválido. Por favor, digite um número.")
        elif choice == '6':
            print("Saindo do programa. Até mais!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

# --- Executa o menu quando o script é iniciado ---
if __name__ == "__main__":
    # Certifique-se de que o servidor está rodando em http://127.0.0.1:5000
    main_menu()