DROP TABLE IF EXISTS tasks;

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'pendente' -- 'pendente', 'em progresso', 'concluída'
);

-- Opcional: Inserir algumas tarefas de exemplo para teste
INSERT INTO
    tasks (title, description, status)
VALUES (
        'Aprender Flask',
        'Estudar a documentação do Flask e suas funcionalidades básicas.',
        'em progresso'
    ),
    (
        'Completar Projeto CRUD',
        'Finalizar o serviço web e a aplicação cliente.',
        'pendente'
    ),
    (
        'Gravar Vídeo',
        'Preparar e gravar a demonstração do projeto.',
        'pendente'
    );