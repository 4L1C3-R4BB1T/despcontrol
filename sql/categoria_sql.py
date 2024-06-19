SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS categoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cor TEXT NOT NULL, 
        id_usuario INTEGER NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id))
"""

SQL_INSERIR = """
    INSERT INTO categoria (nome, cor, id_usuario) 
    VALUES (?, ?, ?)
"""

SQL_OBTER_TODOS = """
    SELECT id, nome
    FROM categoria
    ORDER BY nome
"""

SQL_OBTER_TODOS_POR_USUARIO = """
    SELECT id, nome, cor
    FROM categoria
    WHERE id_usuario=?
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
    SELECT id, nome, cor
    FROM categoria
    WHERE id=?
"""

SQL_OBTER_QUANTIDADE = """
    SELECT COUNT(*) FROM categoria
"""

SQL_OBTER_BUSCA = """
    SELECT id, nome, cor
    FROM categoria
    WHERE nome LIKE ?
    ORDER BY nome
    LIMIT ? OFFSET ?
"""

SQL_OBTER_QUANTIDADE_BUSCA = """
    SELECT COUNT(*) FROM categoria
    WHERE nome LIKE ?
"""

SQL_INSERIR_CATEGORIAS_PADRAO = """
    INSERT INTO categoria (nome, cor, id_usuario) VALUES 
    ('Alimentação', '#FF6347', #1),
    ('Transporte', '#4682B4', #1),
    ('Entretenimento', '#FFD700', #1),
    ('Educação', '#8A2BE2', #1),
    ('Saúde', '#32CD32', #1),
    ('Moradia', '#FF4500', #1),
    ('Vestuário', '#EE82EE', #1),
    ('Lazer', '#20B2AA', #1),
    ('Utilidades', '#808080', #1),
    ('Telecomunicações', '#1E90FF', #1),
    ('Serviços', '#B22222', #1),
    ('Investimentos', '#008000', #1),
    ('Doações', '#FF69B4', #1),
    ('Impostos', '#DC143C', #1),
    ('Seguros', '#0000CD', #1),
    ('Manutenção', '#8B4513', #1),
    ('Viagens', '#FF8C00', #1),
    ('Pets', '#DA70D6', #1),
    ('Hobbies', '#00FA9A', #1),
    ('Tecnologia', '#7B68EE', #1),
    ('Outros', '#A9A9A9', #1);
"""
