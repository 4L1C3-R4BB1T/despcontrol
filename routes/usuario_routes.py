from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from models.usuario_model import Usuario
from repositories.despesa_repo import DespesaRepo
from util.auth import obter_usuario_logado


router = APIRouter()

templates = Jinja2Templates(directory = "templates")


@router.get("/usuario/despesas")
def get_root(request: Request, usuario_logado: Usuario = Depends(obter_usuario_logado)):
    despesas = DespesaRepo.obter_todos_por_usuario(usuario_logado.id)
    return templates.TemplateResponse(
        "despesas.html",
        {
            "request": request,
            "usuario": usuario_logado,
            "despesas": despesas,
        },
    )


@router.get("/usuario/perfil")
def get_root(request: Request, usuario_logado: Usuario = Depends(obter_usuario_logado)):
    return templates.TemplateResponse(
        "perfil.html",
        {
            "request": request,
            "usuario": usuario_logado,
        },
    )
