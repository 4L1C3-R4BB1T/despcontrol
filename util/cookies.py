def adicionar_cookie_tema(response, tema):
    response.set_cookie(
        key="tema",
        value=tema.lower(),
        httponly=True,
        expires="2099-01-01T00:00:00Z",
        samesite="lax",
    )
    return response


def adicionar_mensagem_sucesso(response, mensagem):
    response.set_cookie(
        key="message_success", value=mensagem, max_age=1, httponly=True, samesite="lax"
    )
    return response


def adicionar_mensagem_alerta(response, mensagem):
    response.set_cookie(
        key="message_warning", value=mensagem, max_age=1, httponly=True, samesite="lax"
    )
    return response


def adicionar_mensagem_erro(response, mensagem):
    response.set_cookie(
        key="message_danger", value=mensagem, max_age=1, httponly=True, samesite="lax"
    )
    return response


def adicionar_cookie_auth(response, token):
    response.set_cookie(
        key="auth_token", value=token, max_age=1800, httponly=True, samesite="lax"
    )
    return response
