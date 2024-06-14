from pydantic import BaseModel, field_validator

from util.validators import *


class NovoUsuarioDTO(BaseModel):
    nome: str
    email: str
    senha: str
    confirmacao_senha: str

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

    @field_validator("senha")
    def validar_senha(cls, v):
        msg = is_not_empty(v, "Senha")
        if not msg:
            msg = is_password(v, "Senha")
        if msg:
            raise ValueError(msg.strip())
        return v

    @field_validator("confirmacao_senha")
    def validar_confirmacao_senha(cls, v, values):
        msg = is_not_empty(v, "Confirmação de Senha")
        if "senha" in values.data:
            msg = is_matching_fields(
                v, "Confirmação de Senha", values.data["senha"], "Senha"
            )
        else:
            msg = "Senha não informada."
        if msg:
            raise ValueError(msg)
        return v
