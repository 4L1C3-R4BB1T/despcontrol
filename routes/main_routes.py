import math
from sqlite3 import DatabaseError
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from dtos.entrar_dto import EntrarDTO
from dtos.novo_usuario_dto import NovoUsuarioDTO
from ler_html import ler_html
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from repositories.despesa_repo import DespesaRepo
from util.auth import conferir_senha, gerar_token, obter_hash_senha

from util.cookies import adicionar_cookie_auth, adicionar_mensagem_sucesso
from util.pydantic import create_validation_errors

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/html/{arquivo}")
def get_html(arquivo: str):
    response = HTMLResponse(ler_html(arquivo))
    return response


@router.get("/")
def get_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/cadastro")
def get_cadastro(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})


@router.post("/post_cadastro", response_class=JSONResponse)
async def post_cadastro(usuario_dto: NovoUsuarioDTO):
    # Remover campo confirmacao_senha antes de inserir no banco de dados
    usuario_data = usuario_dto.model_dump(exclude={"confirmacao_senha"})
    usuario_data["senha"] = obter_hash_senha(usuario_data["senha"])
    novo_usuario = UsuarioRepo.inserir(Usuario(**usuario_data))
    if not novo_usuario or not novo_usuario.id:
        raise HTTPException(status_code=400, detail="Erro ao cadastrar usuário.")
    return {"redirect": {"url": "/cadastro_realizado"}}


@router.get("/cadastro_realizado")
def get_cadastro_realizado(request: Request):
    return templates.TemplateResponse("cadastro_confirmado.html", {"request": request})


@router.get("/entrar")
async def get_entrar(request: Request, return_url: str = Query("/")):
    return templates.TemplateResponse(
        "entrar.html", {"request": request, "return_url": return_url}
    )


@router.post("/post_entrar", response_class=JSONResponse)
async def post_entrar(entrar_dto: EntrarDTO):
    usuario_entrou = UsuarioRepo.obter_por_email(entrar_dto.email)
    if (
        (not usuario_entrou)
        or (not usuario_entrou.senha)
        or (not conferir_senha(entrar_dto.senha, usuario_entrou.senha))
    ):
        return JSONResponse(
            content=create_validation_errors(
                entrar_dto,
                ["email", "senha"],
                ["Credenciais inválidas.", "Credenciais inválidas."],
            ),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    token = gerar_token()
    if not UsuarioRepo.alterar_token(usuario_entrou.id, token):
        raise DatabaseError(
            "Não foi possível alterar o token do usuário no banco de dados."
        )
    response = JSONResponse(content={"redirect": {"url": entrar_dto.return_url}})
    adicionar_mensagem_sucesso(
        response,
        f"Olá, <b>{usuario_entrou.nome}</b>. Seja bem-vindo(a) ao DespControl!",
    )
    adicionar_cookie_auth(response, token)
    return response
