from dataclasses import dataclass
from typing import Optional


@dataclass
class Despesa:
    id: Optional[int] = None
    descricao: Optional[str] = None
    valor: Optional[float] = None
    data: Optional[str] = None
    id_categoria: Optional[int] = None
    id_usuario: Optional[int] = None
    nome_categoria: Optional[str] = None
