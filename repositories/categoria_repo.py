import json
import sqlite3
from typing import List, Optional
from models.categoria_model import Categoria
from sql.categoria_sql import *
from util.database import obter_conexao


class CategoriaRepo:

    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA)

    @classmethod
    def inserir(cls, categoria: Categoria) -> Optional[Categoria]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR,
                    (
                        categoria.nome, 
                        categoria.cor, 
                        categoria.id_usuario,
                    ),
                )
                if cursor.rowcount > 0:
                    categoria.id = cursor.lastrowid
                    return categoria
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_todos(cls) -> List[Categoria]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_TODOS).fetchall()
                categorias = [Categoria(*t) for t in tuplas]
                return categorias
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_todos_por_usuario(cls, usuario_id: int) -> List[Categoria]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_TODOS_POR_USUARIO, (usuario_id,)).fetchall()
                categorias = [Categoria(*t) for t in tuplas]
                return categorias
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_todos_por_usuario_paginado(cls, pagina: int, tamanho_pagina: int, usuario_id: int) -> Optional[Categoria]:
        offset = (pagina - 1) * tamanho_pagina
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_TODOS_POR_USUARIO_PAGINADO, (usuario_id, tamanho_pagina, offset)).fetchall()
                categorias = [Categoria(*t) for t in tuplas]
                return categorias
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def alterar(cls, categoria: Categoria) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_ALTERAR,
                    (categoria.nome, categoria.cor),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def excluir(cls, id: int) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_EXCLUIR, (id,))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def obter_um(cls, id: int) -> Optional[Categoria]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_UM, (id,)).fetchone()
                categoria = Categoria(*tupla)
                return categoria
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_quantidade(cls) -> Optional[int]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_QUANTIDADE).fetchone()
                return int(tupla[0])
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_quantidade_por_usuario(cls, usuario_id: int) -> Optional[int]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_QUANTIDADE_POR_USUARIO, (usuario_id,)).fetchone()
                return int(tupla[0])
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def inserir_categorias_json(cls, arquivo_json: str):
        if CategoriaRepo.obter_quantidade() == 0:
            with open(arquivo_json, "r", encoding="utf-8") as arquivo:
                categorias = json.load(arquivo)
                for categoria in categorias:
                    CategoriaRepo.inserir(Categoria(**categoria))

    @classmethod
    def inserir_categorias_padrao(cls, usuario_id: int) -> Optional[Categoria]:
        SQL_INSERIR_CATEGORIAS = SQL_INSERIR_CATEGORIAS_PADRAO.replace("#1", f"{usuario_id}")
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_INSERIR_CATEGORIAS)
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return None
