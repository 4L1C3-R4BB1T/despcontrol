from pydantic import BaseModel, field_validator

from util.validators import *


class NovaDespesaDTO(BaseModel):
    descricao: str
    valor: float
    data: str
    id_categoria: int
    id_usuario: int = None

    @field_validator("descricao")
    def validar_descricao(cls, v):
        msg = is_not_empty(v, "Descrição")
        if msg:
            raise ValueError(msg)
        return v

    @field_validator("valor")
    def validar_valor(cls, v):
        msg = is_greater_than(float(v), "Valor", 0)
        if msg:
            raise ValueError(msg)
        return v

    @field_validator("data")
    def validar_data(cls, v):
        msg = is_not_empty(v, "Data")
        if not msg:
            msg = is_date_valid(v, "Data")
        if msg:
            raise ValueError(msg)
        return v

    @field_validator("id_categoria")
    def validar_categoria(cls, v):
        msg = is_selected_id_valid(v, "Categoria")
        if msg:
            raise ValueError(msg)
        return v
