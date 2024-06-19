from pydantic import BaseModel, field_validator

from util.validators import *


class NovaDCategoriaDTO(BaseModel):
    nome: str
    cor: str
    id_usuario: int = None

    @field_validator("nome")
    def validar_nome(cls, v):
        msg = is_not_empty(v, "Nome")
        if msg:
            raise ValueError(msg)
        return v

    @field_validator("cor")
    def validar_cor(cls, v):
        msg = is_not_empty(v, "Cor")
        if msg:
            raise ValueError(msg)
        return v
