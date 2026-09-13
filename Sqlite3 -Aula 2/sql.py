import sqlite3

conexao = sqlite3.connect("buffet.db")
cursor = conexao.cursor()

# OBRIGATÓRIO no SQLite para validar integridade referencial
cursor.execute("PRAGMA foreign_keys = ON;")
cursor.executescript(
    """
    -- 1. Clientes
    CREATE TABLE IF NOT EXISTS clientes (
        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE,
        endereco TEXT
    );

    -- 2. Usuários do Sistema
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        num_usuario TEXT UNIQUE,
        senha TEXT NOT NULL,
        estado_login TEXT,
        data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP
    );

    -- 3. Informações de Envio
    CREATE TABLE IF NOT EXISTS info_envios (
        num_envio INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo_envio TEXT NOT NULL,
        custo_envio REAL,
        num_regiao_envio INTEGER
    );

    -- 4. Pedidos (conecta Cliente e Envio)
    CREATE TABLE IF NOT EXISTS pedidos (
        num_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER NOT NULL,
        num_envio INTEGER,
        data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
        data_envio TEXT,
        estado TEXT,
        FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente),
        FOREIGN KEY (num_envio) REFERENCES info_envios (num_envio)
    );

    -- 5. Detalhes do Pedido (itens vinculados ao pedido)
    CREATE TABLE IF NOT EXISTS detalhes_pedido (
        num_pedido INTEGER,
        num_produto INTEGER,
        nome_produto TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        custo_unidade REAL NOT NULL,
        subtotal REAL GENERATED ALWAYS AS (quantidade * custo_unidade) STORED,
        PRIMARY KEY (num_pedido, num_produto),
        FOREIGN KEY (num_pedido) REFERENCES pedidos (num_pedido) ON DELETE CASCADE
    );

    -- 6. Tabela Associativa: Atendimento (N:N entre Cliente e Usuário)
    CREATE TABLE IF NOT EXISTS atendimentos (
        id_cliente INTEGER,
        id_usuario INTEGER,
        data_atendimento TEXT DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id_cliente, id_usuario, data_atendimento),
        FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente),
        FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario)
    );
    """
)

conexao.commit()
print("Banco de dados e tabelas do MER criados com sucesso!")
conexao.close()