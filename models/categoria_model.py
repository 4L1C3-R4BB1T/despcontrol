from dataclasses import dataclass
from typing import Optional


@dataclass
class Categoria:
    id: Optional[int] = None
    nome: Optional[str] = None
