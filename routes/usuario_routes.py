import math
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse

from dtos.alterar_categoria_dto import AlterarCategoriaDTO
from dtos.alterar_despesa_dto import AlterarDespesaDTO
from dtos.alterar_senha_dto import AlterarSenhaDTO
from dtos.alterar_usuario_dto import AlterarUsuarioDTO
from dtos.nova_categoria import NovaDCategoriaDTO
from dtos.nova_despesa_dto import NovaDespesaDTO
from models.categoria_model import Categoria
from models.despesa_model import Despesa
from models.usuario_model import Usuario
from repositories.categoria_repo import CategoriaRepo
from repositories.despesa_repo import DespesaRepo
from repositories.usuario_repo import UsuarioRepo
from util.auth import checar_autorizacao, conferir_senha, obter_hash_senha
from util.cookies import adicionar_mensagem_erro, adicionar_mensagem_sucesso, excluir_cookie_auth
from util.templates import obter_jinja_templates


router = APIRouter(prefix="/usuario", tags=["Usuario"])

templates = obter_jinja_templates("templates/usuario")


@router.get("/perfil")
def get_perfil(request: Request):
    checar_autorizacao(request)
    return templates.TemplateResponse("pages/perfil.html", {"request": request})


@router.post("/post_perfil", response_class=JSONResponse)
async def post_dados(request: Request, alterar_dto: AlterarUsuarioDTO):
    checar_autorizacao(request)
    id = request.state.usuario.id
    usuario_data = alterar_dto.model_dump()
    response = JSONResponse({"redirect": {"url": "/usuario/perfil"}})
    if UsuarioRepo.alterar(Usuario(id, **usuario_data)):
        adicionar_mensagem_sucesso(response, "Dados alterados com sucesso!")
    else:
        adicionar_mensagem_erro(response, "Não foi possível alterar os dados cadastrais!")
    return response


@router.get("/senha")
async def get_senha(request: Request):
    checar_autorizacao(request)
    return templates.TemplateResponse("pages/senha_usuario.html", {"request": request})


@router.post("/post_senha", response_class=JSONResponse)
async def post_senha(request: Request, alterar_dto: AlterarSenhaDTO):
    checar_autorizacao(request)
    email = request.state.usuario.email
    usuario_bd = UsuarioRepo.obter_por_email(email)
    nova_senha_hash = obter_hash_senha(alterar_dto.nova_senha)
    response = JSONResponse({"redirect": {"url": "/usuario/senha"}})
    if not conferir_senha(alterar_dto.senha, usuario_bd.senha):
        adicionar_mensagem_erro(response, "Senha atual incorreta!")
        return response
    if UsuarioRepo.alterar_senha(usuario_bd.id, nova_senha_hash):
        adicionar_mensagem_sucesso(response, "Senha alterada com sucesso!")
    else:
        adicionar_mensagem_erro(response, "Não foi possível alterar sua senha!")
    return response


@router.get("/despesas")
def get_despesas(request: Request, p: int = 1, tp: int = 8):
    checar_autorizacao(request)
    usuario_id = request.state.usuario.id
    despesas = DespesaRepo.obter_todos_por_usuario(p, tp, usuario_id)
    categorias = CategoriaRepo.obter_todos_por_usuario(usuario_id)
    qtde_despesas = DespesaRepo.obter_quantidade_por_usuario(usuario_id)
    qtde_paginas = math.ceil(qtde_despesas / float(tp))
    total_gasto = DespesaRepo.obter_total_gasto(usuario_id)
    return templates.TemplateResponse(
        "pages/despesas.html",
        {
            "request": request,
            "despesas": despesas,
            "categorias": categorias,
            "quantidade_paginas": qtde_paginas,
            "tamanho_pagina": tp,
            "pagina_atual": p,
            "total_gasto": total_gasto,
        },
    )


@router.post("/post_cadastro_despesa", response_class=JSONResponse)
async def post_cadastro_despesa(request: Request, despesa: NovaDespesaDTO):
    checar_autorizacao(request)
    despesa_data = despesa.model_dump()
    despesa_data["id_usuario"] = request.state.usuario.id
    nova_despesa = DespesaRepo.inserir(Despesa(**despesa_data))
    if not nova_despesa or not nova_despesa.id:
        raise HTTPException(status_code=400, detail="Erro ao cadastrar despesa.")
    response = JSONResponse(content={"redirect": {"url": "/usuario/despesas"}})
    adicionar_mensagem_sucesso(response, "Despesa cadastrada com sucesso.")
    return response


@router.get("/alterar_despesa/{id_despesa}")
def get_alterar_despesa(request: Request, id_despesa: int):
    checar_autorizacao(request)
    despesa = DespesaRepo.obter_um(id_despesa)
    categorias = CategoriaRepo.obter_todos_por_usuario(request.state.usuario.id)
    return templates.TemplateResponse(
        "pages/alterar_despesa.html",
        {
            "request": request,
            "despesa": despesa,
            "categorias": categorias,
        },
    )


@router.post("/post_alterar_despesa/{id_despesa}", response_class=JSONResponse)
async def post_alterar_despesa(request: Request, despesa: AlterarDespesaDTO):
    checar_autorizacao(request)
    despesa_data = despesa.model_dump()
    despesa_atualizada = DespesaRepo.alterar(Despesa(**despesa_data))
    if not despesa_atualizada:
        raise HTTPException(status_code=400, detail="Erro ao editar despesa.")
    response = JSONResponse(content={"redirect": {"url": "/usuario/despesas"}})
    adicionar_mensagem_sucesso(response, "Despesa atualizada com sucesso.")
    return response


@router.get("/excluir_despesa/{id_despesa}")
def get_excluir_despesa(request: Request, id_despesa: int):
    checar_autorizacao(request)
    despesa = DespesaRepo.obter_um(id_despesa)
    return templates.TemplateResponse(
        "pages/excluir_despesa.html",
        {"request": request, "despesa": despesa},
    )


@router.post("/post_excluir_despesa/{id_despesa}")
async def post_excluir_despesa(request: Request, id_despesa: int):
    checar_autorizacao(request)
    if not DespesaRepo.excluir(id_despesa):
        raise HTTPException(status_code=400, detail="Erro ao excluir despesa.")
    response = JSONResponse(content={"redirect": {"url": "/usuario/despesas"}})
    adicionar_mensagem_sucesso(response, "Despesa excluída com sucesso.")
    return response


@router.get("/categorias")
def get_despesas(request: Request, p: int = 1, tp: int = 9):
    checar_autorizacao(request)
    usuario_id = request.state.usuario.id
    categorias = CategoriaRepo.obter_todos_por_usuario_paginado(p, tp, usuario_id)
    qtde_categorias = CategoriaRepo.obter_quantidade_por_usuario(usuario_id)
    qtde_paginas = math.ceil(qtde_categorias / float(tp))
    return templates.TemplateResponse(
        "pages/categorias.html",
        {
            "request": request,
            "categorias": categorias,
            "quantidade_paginas": qtde_paginas,
            "tamanho_pagina": tp,
            "pagina_atual": p,
        },
    )


@router.post("/post_cadastro_categoria", response_class=JSONResponse)
async def post_cadastro_despesa(request: Request, categoria: NovaDCategoriaDTO):
    checar_autorizacao(request)
    categoria_data = categoria.model_dump()
    categoria_data["id_usuario"] = request.state.usuario.id
    nova_categoria = CategoriaRepo.inserir(Categoria(**categoria_data))
    if not nova_categoria or not nova_categoria.id:
        raise HTTPException(status_code=400, detail="Erro ao cadastrar categoria.")
    response = JSONResponse(content={"redirect": {"url": "/usuario/categorias"}})
    adicionar_mensagem_sucesso(response, "Categoria cadastrada com sucesso.")
    return response


@router.get("/alterar_categoria/{id_categoria}")
def get_alterar_categoria(request: Request, id_categoria: int):
    checar_autorizacao(request)
    categoria = CategoriaRepo.obter_um(id_categoria)
    return templates.TemplateResponse(
        "pages/alterar_categoria.html",
        {
            "request": request,
            "categoria": categoria,
        },
    )


@router.post("/post_alterar_categoria/{id_categoria}", response_class=JSONResponse)
async def post_alterar_categoria(request: Request, categoria: AlterarCategoriaDTO):
    checar_autorizacao(request)
    categoria_data = categoria.model_dump()
    categoria_atualizada = CategoriaRepo.alterar(Categoria(**categoria_data))
    if not categoria_atualizada:
        raise HTTPException(status_code=400, detail="Erro ao editar categoria.")
    response = JSONResponse(content={"redirect": {"url": "/usuario/categorias"}})
    adicionar_mensagem_sucesso(response, "Categoria atualizada com sucesso.")
    return response


@router.get("/excluir_categoria/{id_categoria}")
def get_excluir_categoria(request: Request, id_categoria: int):
    checar_autorizacao(request)
    categoria = CategoriaRepo.obter_um(id_categoria)
    return templates.TemplateResponse(
        "pages/excluir_categoria.html",
        {
            "request": request, 
            "categoria": categoria
        },
    )


@router.post("/post_excluir_categoria/{id_categoria}")
async def post_excluir_categoria(request: Request, id_categoria: int):
    checar_autorizacao(request)
    if DespesaRepo.obter_quantidade_por_usuario_categoria(request.state.usuario.id, id_categoria) > 0:
        response = JSONResponse(content={"redirect": {"url": "/usuario/categorias"}})
        adicionar_mensagem_erro(
            response,
            "Erro ao excluir categoria: há despesas associadas a essa categoria. Remova-as primeiro.",
        )
        return response        
    if not CategoriaRepo.excluir(id_categoria):
        raise HTTPException(status_code=400, detail="Erro ao excluir categoria.")
    response = JSONResponse(content={"redirect": {"url": "/usuario/categorias"}})
    adicionar_mensagem_sucesso(response, "Categoria excluída com sucesso.")
    return response


@router.get("/buscar")
def get_buscar(request: Request, q: str, p: int = 1, tp: int = 8):
    checar_autorizacao(request)
    usuario_id = request.state.usuario.id
    despesas = DespesaRepo.obter_busca(q, p, tp, usuario_id)
    categorias = CategoriaRepo.obter_todos_por_usuario(usuario_id)
    qtde_despesas = DespesaRepo.obter_quantidade_busca(q, usuario_id)
    qtde_paginas = math.ceil(qtde_despesas / float(tp))
    total_gasto = DespesaRepo.obter_total_gasto_busca(q, usuario_id)
    return templates.TemplateResponse(
        "pages/despesas.html",
        {
            "request": request,
            "despesas": despesas,
            "categorias": categorias,
            "quantidade_paginas": qtde_paginas,
            "tamanho_pagina": tp,
            "pagina_atual": p,
            "termo_busca": q,
            "total_gasto": total_gasto,
        },
    )


@router.get("/sair", response_class=RedirectResponse)
async def get_sair(request: Request):
    checar_autorizacao(request)
    if request.state.usuario:
        UsuarioRepo.alterar_token(request.state.usuario.email, "")
    response = RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    excluir_cookie_auth(response)
    adicionar_mensagem_sucesso(response, "Saída realizada com sucesso.")
    return response
