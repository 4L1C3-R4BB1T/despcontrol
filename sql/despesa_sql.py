SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS despesa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        valor FLOAT NOT NULL,
        data DATETIME NOT NULL,
        id_categoria INTEGER NOT NULL,
        id_usuario INTEGER NOT NULL,
        FOREIGN KEY (id_categoria) REFERENCES categoria(id)
        FOREIGN KEY (id_usuario) REFERENCES usuario(id))
"""

SQL_INSERIR = """
    INSERT INTO despesa (descricao, valor, data, id_categoria, id_usuario)
    VALUES (?, ?, ?, ?, ?)
"""

SQL_OBTER_TODOS = """
    SELECT id, descricao, valor, data, id_categoria, id_usuario, categoria.nome AS nome_categoria
    FROM despesa 
    INNER JOIN categoria ON id_categoria = categoria.id
    INNER JOIN usuario ON id_usuario = usuario.id
    ORDER BY data DESC
"""

SQL_ALTERAR = """
    UPDATE despesa
    SET descricao=?, valor=?, data=?, id_categoria=?
    WHERE id=?
"""

SQL_EXCLUIR = """
    DELETE FROM despesa    
    WHERE id=?
"""

SQL_OBTER_UM = """
    SELECT id, descricao, valor, data, id_categoria, id_usuario, categoria.nome AS nome_categoria
    FROM despesa 
    INNER JOIN categoria ON id_categoria = categoria.id
    INNER JOIN usuario ON id_usuario = usuario.id
    WHERE id=?
"""

SQL_OBTER_QUANTIDADE = """
    SELECT COUNT(*) FROM despesa
"""

SQL_OBTER_PERIODO = """
    SELECT id, descricao, valor, data, id_categoria, id_usuario, categoria.nome AS nome_categoria
    FROM despesa 
    INNER JOIN categoria ON id_categoria = categoria.id
    INNER JOIN usuario ON id_usuario = usuario.id
    WHERE data BETWEEN ? AND ?
    ORDER BY data DESC
"""

SQL_OBTER_QUANTIDADE_PERIODO = """
    SELECT COUNT(*) FROM despesa
    WHERE data BETWEEN ? AND ?
"""

SQL_OBTER_POR_CLIENTE = """
    SELECT id, descricao, valor, data, id_categoria
    FROM despesa
    WHERE (id_usuario = ?) AND (data BETWEEN ? AND ?)
    ORDER BY id DESC
"""