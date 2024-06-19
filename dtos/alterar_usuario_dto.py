from pydantic import BaseModel, field_validator

from util.validators import *


class AlterarUsuarioDTO(BaseModel):
    nome: str
    email: str

    @field_validator("nome")
    def validar_nome(cls, v):
        msg = is_person_fullname(v, "Nome")
        if msg:
            raise ValueError(msg)
        return v

    @field_validator("email")
    def validar_email(cls, v):
        msg = is_email(v, "E-mail")
        if msg:
            raise ValueError(msg)
        return v
