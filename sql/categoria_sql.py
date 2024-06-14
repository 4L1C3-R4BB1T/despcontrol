SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS categoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL)
"""

SQL_INSERIR = """
    INSERT INTO categoria (nome) 
    VALUES (?)
"""

SQL_OBTER_TODOS = """
    SELECT id, nome
    FROM categoria
    ORDER BY nome
"""

SQL_ALTERAR = """
    UPDATE categoria
    SET nome=?
    WHERE id=?
"""

SQL_EXCLUIR = """
    DELETE FROM categoria    
    WHERE id=?
"""

SQL_OBTER_UM = """
    SELECT id, nome
    FROM categoria
    WHERE id=?
"""

SQL_OBTER_QUANTIDADE = """
    SELECT COUNT(*) FROM categoria
"""

SQL_OBTER_BUSCA = """
    SELECT id, nome
    FROM categoria
    WHERE nome LIKE ?
    ORDER BY nome
    LIMIT ? OFFSET ?
"""

SQL_OBTER_QUANTIDADE_BUSCA = """
    SELECT COUNT(*) FROM categoria
    WHERE nome LIKE ?
"""
