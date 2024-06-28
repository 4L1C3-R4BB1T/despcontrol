from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from repositories.categoria_repo import CategoriaRepo
from repositories.despesa_repo import DespesaRepo
from repositories.usuario_repo import UsuarioRepo
from routes import main_routes, usuario_routes
from util.auth import middleware_autenticacao
from util.exceptions import configurar_excecoes


UsuarioRepo.criar_tabela()
UsuarioRepo.inserir_usuarios_json("sql/usuarios.json")

CategoriaRepo.criar_tabela()
CategoriaRepo.inserir_categorias_json("sql/categorias.json")

DespesaRepo.criar_tabela()
DespesaRepo.inserir_despesas_json("sql/despesas.json")


app = FastAPI()

app.mount(path="/static", app=StaticFiles(directory="static"), name="static")

app.middleware(middleware_type="http")(middleware_autenticacao)

configurar_excecoes(app)

app.include_router(main_routes.router)
app.include_router(usuario_routes.router)


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app="main:app", port=8000, reload=True)
