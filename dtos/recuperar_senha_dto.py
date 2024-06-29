from pydantic import BaseModel, field_validator

from util.validators import *


class RecuperarSenhaDTO(BaseModel):
    email: str
    nova_senha: str
    confirmacao_nova_senha: str

    @field_validator("email")
    def validar_email(cls, v):
        msg = is_email(v, "E-mail")
        if msg:
            raise ValueError(msg)
        return v

    @field_validator("nova_senha")
    def validar_nova_senha(cls, v):
        msg = is_not_empty(v, "Nova Senha")
        if not msg:
            msg = is_password(v, "Nova Senha")
        if msg:
            raise ValueError(msg.strip())
        return v

    @field_validator("confirmacao_nova_senha")
    def validar_confirmacao_nova_senha(cls, v, values):
        msg = is_not_empty(v, "Confirmação de Nova Senha")
        if "nova_senha" in values.data:
            msg = is_matching_fields(
                v, "Confirmação de Nova Senha", values.data["nova_senha"], "Nova Senha"
            )
        else:
            msg = "Nova senha não informada."
        if msg:
            raise ValueError(msg)
        return v
