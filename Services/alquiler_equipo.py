"""
Servicio especializado: Alquiler de Equipos tecnológicos.
Hereda de Servicio e implementa lógica de inventario y tipo de equipo.
"""

from models.servicio import Servicio
from exceptions.custom_exceptions import (
    ServicioParametroInvalidoError,
    ServicioNoDisponibleError,
)

TIPOS_VALIDOS = {"laptop", "proyector", "tablet", "servidor", "camara"}


class AlquilerEquipo(Servicio):
    """
    Servicio de alquiler de equipos tecnológicos en Software FJ.
    Aplica cargo extra por equipos de alta gama y controla stock disponible.
    """

    PRECIO_BASE_HORA: float = 45_000.0  # COP por hora

    def __init__(
        self,
        nombre: str = "Alquiler de Equipo",
        tipo_equipo: str = "laptop",
        cantidad_disponible: int = 5,
        alta_gama: bool = False,
        precio_hora: float = None,
        disponible: bool = True,
    ):
        """
        Args:
            nombre:               Nombre descriptivo del equipo.
            tipo_equipo:          Tipo de equipo (laptop, proyector, tablet, etc.).
            cantidad_disponible:  Unidades disponibles en inventario.
            alta_gama:            Si True, aplica recargo del 50 %.
            precio_hora:          Precio personalizado; si None, usa PRECIO_BASE_HORA.
            disponible:           Disponibilidad del servicio.

        Raises:
            ServicioParametroInvalidoError: Si tipo_equipo o cantidad no son válidos.
        """
        tipo_lower = tipo_equipo.lower().strip() if isinstance(tipo_equipo, str) else ""
        if tipo_lower not in TIPOS_VALIDOS:
            raise ServicioParametroInvalidoError("tipo_equipo", tipo_equipo)
        if not isinstance(cantidad_disponible, int) or cantidad_disponible < 0:
            raise ServicioParametroInvalidoError("cantidad_disponible", cantidad_disponible)

        precio = precio_hora if precio_hora else self.PRECIO_BASE_HORA
        if alta_gama:
            precio *= 1.50

        super().__init__(nombre, precio, disponible)
        self.__tipo_equipo: str = tipo_lower
        self.__cantidad_disponible: int = cantidad_disponible
        self.__alta_gama: bool = alta_gama

    # ── Propiedades ───────────────────────────────────────

    @property
    def tipo_equipo(self) -> str:
        return self.__tipo_equipo

    @property
    def cantidad_disponible(self) -> int:
        return self.__cantidad_disponible

    @property
    def alta_gama(self) -> bool:
        return self.__alta_gama

    # ── Métodos de negocio ────────────────────────────────

    def reservar_unidades(self, cantidad: int) -> None:
        """
        Descuenta unidades del inventario al efectuar una reserva.

        Raises:
            ServicioParametroInvalidoError: Si cantidad es inválida.
            ServicioNoDisponibleError:       Si no hay stock suficiente.
        """
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ServicioParametroInvalidoError("cantidad", cantidad)
        if cantidad > self.__cantidad_disponible:
            raise ServicioNoDisponibleError(
                f"{self.nombre} (solicitan {cantidad}, disponibles {self.__cantidad_disponible})"
            )
        self.__cantidad_disponible -= cantidad

    def liberar_unidades(self, cantidad: int) -> None:
        """Devuelve unidades al inventario al cancelar una reserva."""
        if isinstance(cantidad, int) and cantidad > 0:
            self.__cantidad_disponible += cantidad

    # ── Implementación de métodos abstractos (polimorfismo) ──

    def calcular_costo(self, horas: int, cantidad: int = 1) -> float:
        """Costo = precio_hora × horas × cantidad de equipos."""
        self._validar_horas(horas)
        return self.precio_hora * horas * max(1, cantidad)

    def calcular_costo_con_impuesto(
        self, horas: int, tasa_impuesto: float = 0.19, cantidad: int = 1
    ) -> float:
        """Costo con IVA incluido para N equipos."""
        self._validar_horas(horas)
        base = self.calcular_costo(horas, cantidad)
        return base * (1 + tasa_impuesto)

    def calcular_costo_con_descuento(
        self, horas: int, descuento: float = 0.0, cantidad: int = 1
    ) -> float:
        """Costo con descuento porcentual para N equipos."""
        self._validar_horas(horas)
        if not (0 <= descuento < 1):
            raise ServicioParametroInvalidoError("descuento", descuento)
        base = self.calcular_costo(horas, cantidad)
        return base * (1 - descuento)

    def validar_parametros(self, cantidad: int = 1, **kwargs) -> bool:
        """Verifica disponibilidad de stock para la cantidad solicitada."""
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ServicioParametroInvalidoError("cantidad", cantidad)
        if cantidad > self.__cantidad_disponible:
            raise ServicioNoDisponibleError(
                f"{self.nombre} — stock insuficiente ({self.__cantidad_disponible} disponibles)"
            )
        return True

    # ── Utilidades internas ───────────────────────────────

    @staticmethod
    def _validar_horas(horas: int) -> None:
        if not isinstance(horas, int) or horas <= 0:
            raise ServicioParametroInvalidoError("horas", horas)

    # ── Contrato Entidad ──────────────────────────────────

    def describir(self) -> str:
        gama = "Alta Gama" if self.__alta_gama else "Estándar"
        return (
            f"{super().describir()} | Tipo: {self.__tipo_equipo.capitalize()} | "
            f"Stock: {self.__cantidad_disponible} | Gama: {gama}"
        )
