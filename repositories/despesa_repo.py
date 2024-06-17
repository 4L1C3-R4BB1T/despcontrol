import json
import sqlite3
from typing import List, Optional
from models.despesa_model import Despesa
from sql.despesa_sql import *
from util.database import obter_conexao


class DespesaRepo:

    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA)

    @classmethod
    def inserir(cls, despesa: Despesa) -> Optional[Despesa]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR,
                    (
                        despesa.descricao,
                        despesa.valor,
                        despesa.data,
                        despesa.id_categoria,
                        despesa.id_usuario,
                    ),
                )
                if cursor.rowcount > 0:
                    despesa.id = cursor.lastrowid
                    return despesa
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_todos(cls) -> List[Despesa]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_TODOS).fetchall()
                despesas = [Despesa(*t) for t in tuplas]
                return despesas
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def alterar(cls, despesa: Despesa) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_ALTERAR,
                    (
                        despesa.descricao,
                        despesa.valor,
                        despesa.data,
                        despesa.id_categoria,
                        despesa.id,
                    ),
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
    def obter_um(cls, id: int) -> Optional[Despesa]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_UM, (id,)).fetchone()
                despesa = Despesa(*tupla)
                return despesa
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
    def obter_todos_por_usuario(cls, pagina: int, tamanho_pagina: int, usuario_id: int) -> Optional[Despesa]:
        offset = (pagina - 1) * tamanho_pagina
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_TODOS_POR_USUARIO, (usuario_id, tamanho_pagina, offset)).fetchall()
                despesas = [Despesa(*t) for t in tuplas]
                return despesas
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def inserir_despesas_json(cls, arquivo_json: str):
        if DespesaRepo.obter_quantidade() == 0:
            with open(arquivo_json, "r", encoding="utf-8") as arquivo:
                despesas = json.load(arquivo)
                for despesa in despesas:
                    DespesaRepo.inserir(Despesa(**despesa))
