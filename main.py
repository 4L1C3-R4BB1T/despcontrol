from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from repositories.categoria_repo import CategoriaRepo
from repositories.despesa_repo import DespesaRepo
from repositories.usuario_repo import UsuarioRepo
from routes import main_routes
from util.auth import atualizar_cookie_autenticacao
from util.exceptions import configurar_excecoes


# senha: S3nh@
UsuarioRepo.criar_tabela()
UsuarioRepo.inserir_usuarios_json("sql/usuarios.json")

CategoriaRepo.criar_tabela()
CategoriaRepo.inserir_categorias_json("sql/categorias.json")

DespesaRepo.criar_tabela()
DespesaRepo.inserir_despesas_json("sql/despesas.json")


app = FastAPI()

app.middleware(middleware_type="http")(atualizar_cookie_autenticacao)

configurar_excecoes(app)

app.mount(path="/static", app=StaticFiles(directory="static"), name="static")

app.include_router(main_routes.router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)
