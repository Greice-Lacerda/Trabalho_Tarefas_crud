import sqlite3
from flask import Flask, jsonify, request, g
from flask_cors import CORS # Importar a extensão CORS

# --- Configuração do Flask ---
app = Flask(__name__)
app.config['DATABASE'] = 'tasks.db' # Nome do arquivo do banco de dados SQLite
CORS(app) # Habilita CORS para todas as rotas e todas as origens

# --- Funções de Banco de Dados ---

def get_db():
    """
    Função para obter a conexão com o banco de dados SQLite.
    Reutiliza a conexão se já existir no contexto da requisição (g).
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES
        )
        g.db.row_factory = sqlite3.Row # Retorna linhas como objetos que se comportam como dicionários
    return g.db

def close_db(e=None):
    """
    Função para fechar a conexão com o banco de dados no final da requisição.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """
    Função para inicializar o esquema do banco de dados (criar tabelas).
    """
    db = get_db()
    # Abre o arquivo schema.sql e executa os comandos SQL para criar as tabelas
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    print("Banco de dados inicializado com sucesso!")

# Registra a função close_db para ser executada após cada requisição.
app.teardown_appcontext(close_db)

# --- Rotas da API de Tarefas (CRUD) ---

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Retorna todas as tarefas.
    """
    db = get_db()
    tasks = db.execute('SELECT * FROM tasks').fetchall()
    return jsonify([dict(task) for task in tasks])

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Retorna uma tarefa específica pelo ID.
    """
    db = get_db()
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if task is None:
        return jsonify({'message': 'Tarefa não encontrada'}), 404
    return jsonify(dict(task))

@app.route('/tasks', methods=['POST'])
def create_task():
    """
    Cria uma nova tarefa.
    Espera um JSON com 'title', 'description' (opcional) e 'status' (opcional).
    """
    if not request.is_json:
        return jsonify({"message": "Content-Type must be application/json"}), 400

    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '') # Padrão vazio se não for fornecido
    status = data.get('status', 'pendente')   # Padrão 'pendente' se não for fornecido

    if not title:
        return jsonify({'message': 'O título da tarefa é obrigatório'}), 400

    db = get_db()
    try:
        cursor = db.execute(
            'INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)',
            (title, description, status)
        )
        db.commit()
        # Retorna a tarefa recém-criada (com o ID gerado)
        new_task_id = cursor.lastrowid
        new_task = db.execute('SELECT * FROM tasks WHERE id = ?', (new_task_id,)).fetchone()
        return jsonify(dict(new_task)), 201 # 201 Created
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Erro ao criar tarefa. Título duplicado ou outro problema de integridade.'}), 409
    except Exception as e:
        return jsonify({'message': f'Erro interno ao criar tarefa: {str(e)}'}), 500


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Atualiza uma tarefa existente pelo ID.
    Espera um JSON com 'title', 'description' e/ou 'status'.
    """
    if not request.is_json:
        return jsonify({"message": "Content-Type must be application/json"}), 400

    data = request.get_json()
    db = get_db()
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()

    if task is None:
        return jsonify({'message': 'Tarefa não encontrada'}), 404

    # Pega os valores existentes como padrão se não forem fornecidos na requisição
    title = data.get('title', task['title'])
    description = data.get('description', task['description'])
    status = data.get('status', task['status'])

    try:
        db.execute(
            'UPDATE tasks SET title = ?, description = ?, status = ? WHERE id = ?',
            (title, description, status, task_id)
        )
        db.commit()
        updated_task = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        return jsonify(dict(updated_task))
    except Exception as e:
        return jsonify({'message': f'Erro interno ao atualizar tarefa: {str(e)}'}), 500


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Deleta uma tarefa específica pelo ID.
    """
    db = get_db()
    cursor = db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    db.commit()

    if cursor.rowcount == 0: # rowcount indica o número de linhas afetadas
        return jsonify({'message': 'Tarefa não encontrada'}), 404
    return jsonify({'message': 'Tarefa deletada com sucesso'}), 200 # 200 OK

# --- Bloco de Execução Principal ---
if __name__ == '__main__':
    with app.app_context():
        # Inicializa o banco de dados quando o aplicativo é executado pela primeira vez
        init_db()
    # Inicia o servidor Flask em modo de depuração (debug=True)
    # Ele será acessível em http://127.0.0.1:5000 por padrão
    app.run(debug=True)