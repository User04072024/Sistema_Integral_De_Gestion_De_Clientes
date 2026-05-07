"""
Servicio especializado: Reserva de Sala de reuniones/trabajo.
Hereda de Servicio e implementa polimorfismo con lógica propia.
"""

from models.servicio import Servicio
from exceptions.custom_exceptions import (
    ServicioCapacidadExcedidaError,
    ServicioParametroInvalidoError,
)


class ReservaSala(Servicio):
    """
    Servicio de reserva de salas de reunión o trabajo en Software FJ.
    Aplica recargo por sala premium y validación de capacidad de personas.
    """

    PRECIO_BASE_HORA: float = 80_000.0   # COP por hora
    CAPACIDAD_MAXIMA: int = 30

    def __init__(
        self,
        nombre: str = "Reserva de Sala",
        capacidad: int = 10,
        es_premium: bool = False,
        precio_hora: float = None,
        disponible: bool = True,
    ):
        """
        Args:
            nombre:     Identificador de la sala (ej. "Sala Innovación").
            capacidad:  Número máximo de personas permitidas.
            es_premium: Si es True, aplica recargo del 30 % sobre el precio base.
            precio_hora: Precio personalizado; si None, usa PRECIO_BASE_HORA.
            disponible:  Disponibilidad del servicio.

        Raises:
            ServicioParametroInvalidoError: Si la capacidad es inválida.
            ServicioCapacidadExcedidaError: Si capacidad > CAPACIDAD_MAXIMA.
        """
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioParametroInvalidoError("capacidad", capacidad)
        if capacidad > self.CAPACIDAD_MAXIMA:
            raise ServicioCapacidadExcedidaError(nombre, self.CAPACIDAD_MAXIMA)

        precio = precio_hora if precio_hora else self.PRECIO_BASE_HORA
        if es_premium:
            precio *= 1.30  # recargo premium

        super().__init__(nombre, precio, disponible)
        self.__capacidad: int = capacidad
        self.__es_premium: bool = es_premium

    # ── Propiedades ───────────────────────────────────────

    @property
    def capacidad(self) -> int:
        return self.__capacidad

    @property
    def es_premium(self) -> bool:
        return self.__es_premium

    # ── Implementación de métodos abstractos (polimorfismo) ──

    def calcular_costo(self, horas: int) -> float:
        """Costo base = precio_hora × horas."""
        self._validar_horas(horas)
        return self.precio_hora * horas

    def calcular_costo_con_impuesto(self, horas: int, tasa_impuesto: float = 0.19) -> float:
        """Costo con IVA incluido."""
        self._validar_horas(horas)
        self._validar_tasa(tasa_impuesto)
        base = self.calcular_costo(horas)
        return base * (1 + tasa_impuesto)

    def calcular_costo_con_descuento(self, horas: int, descuento: float = 0.0) -> float:
        """Costo con descuento porcentual (0.0 – 1.0)."""
        self._validar_horas(horas)
        self._validar_descuento(descuento)
        base = self.calcular_costo(horas)
        return base * (1 - descuento)

    def validar_parametros(self, personas: int = 1, **kwargs) -> bool:
        """
        Valida que el número de personas no supere la capacidad.

        Raises:
            ServicioParametroInvalidoError: Si personas <= 0.
            ServicioCapacidadExcedidaError: Si personas > capacidad.
        """
        if not isinstance(personas, int) or personas <= 0:
            raise ServicioParametroInvalidoError("personas", personas)
        if personas > self.__capacidad:
            raise ServicioCapacidadExcedidaError(self.nombre, self.__capacidad)
        return True

    # ── Utilidades internas ───────────────────────────────

    @staticmethod
    def _validar_horas(horas: int) -> None:
        if not isinstance(horas, int) or horas <= 0:
            raise ServicioParametroInvalidoError("horas", horas)

    @staticmethod
    def _validar_tasa(tasa: float) -> None:
        if not isinstance(tasa, (int, float)) or not (0 <= tasa <= 1):
            raise ServicioParametroInvalidoError("tasa_impuesto", tasa)

    @staticmethod
    def _validar_descuento(descuento: float) -> None:
        if not isinstance(descuento, (int, float)) or not (0 <= descuento < 1):
            raise ServicioParametroInvalidoError("descuento", descuento)

    # ── Contrato Entidad ──────────────────────────────────

    def describir(self) -> str:
        tipo = "PREMIUM" if self.__es_premium else "Estándar"
        return (
            f"{super().describir()} | Capacidad: {self.__capacidad} personas | "
            f"Tipo: {tipo}"
        )
