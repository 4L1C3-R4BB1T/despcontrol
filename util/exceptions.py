import logging
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from models.usuario_model import Usuario
from util.cookies import adicionar_mensagem_erro
from util.auth import obter_usuario_logado

templates = Jinja2Templates(directory="templates")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def configurar_excecoes(app: FastAPI):
    @app.exception_handler(401)
    async def unauthorized_exception_handler(request: Request, _):
        return_url = f"?return_url={request.url.path}"
        response = RedirectResponse(
            f"/entrar{return_url}", status_code=status.HTTP_302_FOUND
        )
        adicionar_mensagem_erro(
            response,
            f"A página {request.url.path} é restrita a usuários logados. Identifique-se para poder prosseguir.",
        )
        return response

    @app.exception_handler(403)
    async def forbidden_exception_handler(request: Request, _):
        usuario = await obter_usuario_logado(request)
        return_url = f"?return_url={request.url.path}"
        response = RedirectResponse(
            f"/entrar{return_url}", status_code=status.HTTP_302_FOUND
        )
        adicionar_mensagem_erro(
            response,
            f"Você está logado como <b>{usuario.nome}</b> e seu perfil de usuário não tem autorização de acesso à página <b>{request.url.path}</b>. Entre com um usuário do perfil adequado para poder acessar a página em questão.",
        )
        return response

    @app.exception_handler(404)
    async def page_not_found_exception_handler(
        request: Request, usuario_logado=Depends(obter_usuario_logado)
    ):
        return templates.TemplateResponse(
            "404.html", {"request": request, "usuario": usuario_logado}
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        ex: HTTPException,
        usuario_logado: Usuario = Depends(obter_usuario_logado),
    ):
        logger.error("Ocorreu uma exceção não tratada: %s", ex)
        view_model = {
            "request": request,
            "usuario": usuario_logado,
            "detail": "Erro na requisição HTTP.",
        }
        return templates.TemplateResponse(
            "erro.html", view_model, status_code=ex.status_code
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request,
        ex: Exception,
        usuario_logado: Usuario = Depends(obter_usuario_logado),
    ):
        logger.error("Ocorreu uma exceção não tratada: %s", ex)
        view_model = {
            "request": request,
            "usuario": usuario_logado,
            "detail": "Erro interno do servidor.",
        }
        return templates.TemplateResponse("erro.html", view_model, status_code=500)
