from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from dtos.nova_despesa import NovaDespesaDTO
from models.despesa_model import Despesa
from models.usuario_model import Usuario
from repositories.categoria_repo import CategoriaRepo
from repositories.despesa_repo import DespesaRepo
from util.auth import obter_usuario_logado


router = APIRouter()

templates = Jinja2Templates(directory = "templates")


@router.get("/usuario/despesas")
def get_root(request: Request, usuario_logado: Usuario = Depends(obter_usuario_logado)):
    despesas = DespesaRepo.obter_todos_por_usuario(usuario_logado.id)
    categorias = CategoriaRepo.obter_todos()
    return templates.TemplateResponse(
        "despesas.html",
        {
            "request": request,
            "usuario": usuario_logado,
            "despesas": despesas,
            "categorias": categorias,
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


@router.post("/usuario/post_cadastro_despesa", response_class=JSONResponse)
async def post_cadastro(despesa: NovaDespesaDTO, usuario_logado: Usuario = Depends(obter_usuario_logado)):
    despesa_data = despesa.model_dump()
    despesa_data["id_usuario"] = usuario_logado.id
    nova_despesa = DespesaRepo.inserir(Despesa(**despesa_data))
    if not nova_despesa or not nova_despesa.id:
        raise HTTPException(status_code=400, detail="Erro ao cadastrar despesa.")
    return {"redirect": {"url": "/usuario/despesas"}}
