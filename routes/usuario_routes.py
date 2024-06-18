import math
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from dtos.edicao_despesa import EdicaoDespesaDTO
from dtos.nova_despesa import NovaDespesaDTO
from models.despesa_model import Despesa
from models.usuario_model import Usuario
from repositories.categoria_repo import CategoriaRepo
from repositories.despesa_repo import DespesaRepo
from util.auth import obter_usuario_logado
from util.cookies import adicionar_mensagem_sucesso


router = APIRouter()

templates = Jinja2Templates(directory = "templates")


@router.get("/usuario/despesas")
def get_despesas(request: Request, p: int = 1, tp: int = 8, usuario_logado: Usuario = Depends(obter_usuario_logado)):
    despesas = DespesaRepo.obter_todos_por_usuario(p, tp, usuario_logado.id)
    categorias = CategoriaRepo.obter_todos()
    qtde_despesas = DespesaRepo.obter_quantidade_por_usuario(usuario_logado.id)
    qtde_paginas = math.ceil(qtde_despesas / float(tp))
    return templates.TemplateResponse(
        "despesas.html",
        {
            "request": request,
            "usuario": usuario_logado,
            "despesas": despesas,
            "categorias": categorias,
            "quantidade_paginas": qtde_paginas,
            "tamanho_pagina": tp,
            "pagina_atual": p,
        },
    )


@router.get("/usuario/perfil")
def get_usuario_perfil(request: Request, usuario_logado: Usuario = Depends(obter_usuario_logado)):
    return templates.TemplateResponse(
        "perfil.html",
        {
            "request": request,
            "usuario": usuario_logado,
        },
    )


@router.post("/usuario/post_cadastro_despesa", response_class=JSONResponse)
async def post_cadastro_despesa(despesa: NovaDespesaDTO, usuario_logado: Usuario = Depends(obter_usuario_logado)):
    despesa_data = despesa.model_dump()
    despesa_data["id_usuario"] = usuario_logado.id
    nova_despesa = DespesaRepo.inserir(Despesa(**despesa_data))
    if not nova_despesa or not nova_despesa.id:
        raise HTTPException(status_code=400, detail="Erro ao cadastrar despesa.")
    response = JSONResponse(content={"redirect": {"url": "/usuario/despesas"}})
    adicionar_mensagem_sucesso(response, "Despesa cadastrada com sucesso.")
    return response


@router.get("/usuario/despesas/edicao/{id_despesa}")
def get_edicao_despesa(request: Request, id_despesa: int, usuario_logado: Usuario = Depends(obter_usuario_logado)):
    despesa = DespesaRepo.obter_um(id_despesa)
    categorias = CategoriaRepo.obter_todos()
    return templates.TemplateResponse(
        "edicao_despesa.html",
        {
            "request": request,
            "usuario": usuario_logado,
            "despesa": despesa,
            "categorias": categorias,
        },
    )


@router.post("/usuario/post_edicao_despesa", response_class=JSONResponse)
async def post_edicao_despesa(despesa: EdicaoDespesaDTO):
    despesa_data = despesa.model_dump()
    despesa_atualizada = DespesaRepo.alterar(Despesa(**despesa_data))
    if not despesa_atualizada:
        raise HTTPException(status_code=400, detail="Erro ao editar despesa.")
    response = JSONResponse(content={"redirect": {"url": "/usuario/despesas"}})
    adicionar_mensagem_sucesso(response, "Despesa atualizada com sucesso.")
    return response


@router.get("/usuario/buscar")
def get_root(request: Request, q: str, p: int = 1, tp: int = 6, usuario_logado: Usuario = Depends(obter_usuario_logado)):
    despesas = DespesaRepo.obter_busca(q, p, tp, usuario_logado.id)
    categorias = CategoriaRepo.obter_todos()
    qtde_despesas = DespesaRepo.obter_quantidade_busca(q, usuario_logado.id)
    qtde_paginas = math.ceil(qtde_despesas / float(tp))
    return templates.TemplateResponse(
        "despesas.html",
        {
            "request": request,
            "usuario": usuario_logado,
            "despesas": despesas,
            "categorias": categorias,
            "quantidade_paginas": qtde_paginas,
            "tamanho_pagina": tp,
            "pagina_atual": p,
            "termo_busca": q,
        },
    )
