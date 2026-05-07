"""
Módulo que define la clase abstracta base Entidad,
raíz de la jerarquía de objetos del sistema Software FJ.
"""

from abc import ABC, abstractmethod
from datetime import datetime


class Entidad(ABC):
    """
    Clase abstracta base para todas las entidades del sistema.
    Provee identificador único, fecha de creación y contrato
    de métodos que toda entidad debe implementar.
    """

    _contador: int = 0

    def __init__(self, nombre: str):
        Entidad._contador += 1
        self.__id: str = f"ENT-{Entidad._contador:05d}"
        self.__nombre: str = nombre
        self.__fecha_creacion: datetime = datetime.now()

    # ── Propiedades ──────────────────────────────────────

    @property
    def id(self) -> str:
        return self.__id

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = valor

    @property
    def fecha_creacion(self) -> datetime:
        return self.__fecha_creacion

    # ── Métodos abstractos ────────────────────────────────

    @abstractmethod
    def describir(self) -> str:
        """Retorna una descripción legible de la entidad."""

    @abstractmethod
    def validar(self) -> bool:
        """Valida la integridad de los datos de la entidad."""

    # ── Representación ────────────────────────────────────

    def __str__(self) -> str:
        return self.describir()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.__id!r}, nombre={self.__nombre!r})"
