from abc import abstractmethod
from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models import models

class AbstractPokemonRepository:
    @abstractmethod
    def list(self) -> List["Tipo"]:
        raise NotImplementedError
    @abstractmethod
    def get(self, tipo:"Tipo") -> Optional["Tipo"]:
        raise NotImplemented