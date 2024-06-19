SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        token TEXT)
"""

SQL_INSERIR = """
    INSERT INTO usuario (nome, email, senha)
    VALUES (?, ?, ?)
"""

SQL_OBTER_TODOS = """
    SELECT id, nome, email
    FROM usuario
    ORDER BY nome
"""

SQL_ALTERAR = """
    UPDATE usuario
    SET nome=?, email=?
    WHERE id=?
"""

SQL_ALTERAR_TOKEN = """
    UPDATE usuario
    SET token=?
    WHERE id=?
"""

SQL_EXCLUIR = """
    DELETE FROM usuario    
    WHERE id=?
"""

SQL_OBTER_UM = """
    SELECT id, nome, email
    FROM usuario
    WHERE id=?
"""

SQL_OBTER_POR_EMAIL = """
    SELECT id, nome, email, senha
    FROM usuario
    WHERE email=?
"""

SQL_OBTER_POR_TOKEN = """
    SELECT id, nome, email
    FROM usuario
    WHERE token=?
"""

SQL_OBTER_QUANTIDADE = """
    SELECT COUNT(*) FROM usuario
"""

SQL_OBTER_BUSCA = """
    SELECT id, nome, email
    FROM usuario
    WHERE nome LIKE ?
    ORDER BY nome
    LIMIT ? OFFSET ?
"""

SQL_OBTER_QUANTIDADE_BUSCA = """
    SELECT COUNT(*) FROM usuario
    WHERE nome LIKE ?
"""

SQL_ALTERAR_SENHA = """
    UPDATE usuario
    SET senha=?
    WHERE id=?
"""
