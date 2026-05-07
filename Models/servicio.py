"""
Módulo de la clase abstracta Servicio.
Define el contrato que deben implementar todos los servicios
de Software FJ: calcular costos, describir y validar parámetros.
"""

from abc import abstractmethod
from models.entidad import Entidad
from exceptions.custom_exceptions import (
    ServicioPrecioInvalidoError,
    ServicioNoDisponibleError,
)


class Servicio(Entidad):
    """
    Clase abstracta base para todos los servicios de Software FJ.
    Hereda de Entidad y exige implementar métodos de cálculo de costos.
    """

    _contador_servicios: int = 0

    def __init__(self, nombre: str, precio_hora: float, disponible: bool = True):
        """
        Args:
            nombre:       Nombre del servicio.
            precio_hora:  Precio base por hora (debe ser > 0).
            disponible:   Si el servicio está disponible para reserva.

        Raises:
            ServicioPrecioInvalidoError: Si precio_hora <= 0 o no es numérico.
        """
        if not isinstance(precio_hora, (int, float)) or precio_hora <= 0:
            raise ServicioPrecioInvalidoError(precio_hora)

        super().__init__(nombre)

        Servicio._contador_servicios += 1
        self.__id_servicio: str = f"SRV-{Servicio._contador_servicios:04d}"
        self.__precio_hora: float = float(precio_hora)
        self.__disponible: bool = disponible

    # ── Propiedades ───────────────────────────────────────

    @property
    def id_servicio(self) -> str:
        return self.__id_servicio

    @property
    def precio_hora(self) -> float:
        return self.__precio_hora

    @precio_hora.setter
    def precio_hora(self, valor: float) -> None:
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ServicioPrecioInvalidoError(valor)
        self.__precio_hora = float(valor)

    @property
    def disponible(self) -> bool:
        return self.__disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        self.__disponible = bool(valor)

    # ── Métodos abstractos ────────────────────────────────

    @abstractmethod
    def calcular_costo(self, horas: int) -> float:
        """Calcula el costo base del servicio para N horas."""

    @abstractmethod
    def calcular_costo_con_impuesto(self, horas: int, tasa_impuesto: float = 0.19) -> float:
        """Calcula el costo incluyendo impuesto."""

    @abstractmethod
    def calcular_costo_con_descuento(self, horas: int, descuento: float = 0.0) -> float:
        """Calcula el costo aplicando un descuento porcentual."""

    @abstractmethod
    def validar_parametros(self, **kwargs) -> bool:
        """Valida los parámetros específicos del servicio."""

    # ── Método concreto compartido ────────────────────────

    def verificar_disponibilidad(self) -> None:
        """
        Verifica que el servicio esté disponible.

        Raises:
            ServicioNoDisponibleError: Si el servicio no está activo.
        """
        if not self.__disponible:
            raise ServicioNoDisponibleError(self.nombre)

    # ── Contrato Entidad ──────────────────────────────────

    def describir(self) -> str:
        estado = "Disponible" if self.__disponible else "No disponible"
        return (
            f"Servicio [{self.__id_servicio}] | {self.nombre} | "
            f"Precio/hora: ${self.__precio_hora:,.2f} | Estado: {estado}"
        )

    def validar(self) -> bool:
        return self.__precio_hora > 0 and isinstance(self.__disponible, bool)
