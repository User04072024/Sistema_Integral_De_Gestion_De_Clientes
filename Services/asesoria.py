"""
Servicio especializado: Asesoría Especializada.
Hereda de Servicio e implementa lógica de niveles de experiencia
y modalidad (presencial / virtual).
"""

from models.servicio import Servicio
from exceptions.custom_exceptions import ServicioParametroInvalidoError

NIVELES_VALIDOS = {"junior", "senior", "experto"}
MODALIDADES_VALIDAS = {"presencial", "virtual"}


class Asesoria(Servicio):
    """
    Servicio de asesoría especializada en Software FJ.
    El precio varía según el nivel del asesor y la modalidad.
    """

    PRECIO_BASE_HORA: float = 120_000.0   # COP por hora (asesor junior)
    MULTIPLICADOR_NIVEL = {
        "junior":  1.0,
        "senior":  1.6,
        "experto": 2.2,
    }

    def __init__(
        self,
        nombre: str = "Asesoría Especializada",
        area: str = "Tecnología",
        nivel_asesor: str = "junior",
        modalidad: str = "presencial",
        precio_hora: float = None,
        disponible: bool = True,
    ):
        """
        Args:
            nombre:        Nombre/título de la asesoría.
            area:          Área temática (ej. "Seguridad", "Arquitectura de software").
            nivel_asesor:  Nivel del asesor: junior | senior | experto.
            modalidad:     presencial | virtual.
            precio_hora:   Precio base personalizado; si None, usa PRECIO_BASE_HORA × nivel.
            disponible:    Disponibilidad del servicio.

        Raises:
            ServicioParametroInvalidoError: Si nivel_asesor o modalidad son inválidos.
        """
        nivel = nivel_asesor.lower().strip() if isinstance(nivel_asesor, str) else ""
        modalidad_lower = modalidad.lower().strip() if isinstance(modalidad, str) else ""

        if nivel not in NIVELES_VALIDOS:
            raise ServicioParametroInvalidoError("nivel_asesor", nivel_asesor)
        if modalidad_lower not in MODALIDADES_VALIDAS:
            raise ServicioParametroInvalidoError("modalidad", modalidad)

        precio = (
            precio_hora
            if precio_hora
            else self.PRECIO_BASE_HORA * self.MULTIPLICADOR_NIVEL[nivel]
        )
        # Virtual tiene descuento del 10 %
        if modalidad_lower == "virtual":
            precio *= 0.90

        super().__init__(nombre, precio, disponible)
        self.__area: str = area
        self.__nivel_asesor: str = nivel
        self.__modalidad: str = modalidad_lower
        self.__horas_minimas: int = 2 if nivel == "experto" else 1

    # ── Propiedades ───────────────────────────────────────

    @property
    def area(self) -> str:
        return self.__area

    @property
    def nivel_asesor(self) -> str:
        return self.__nivel_asesor

    @property
    def modalidad(self) -> str:
        return self.__modalidad

    @property
    def horas_minimas(self) -> int:
        return self.__horas_minimas

    # ── Implementación de métodos abstractos (polimorfismo) ──

    def calcular_costo(self, horas: int) -> float:
        """Costo base = precio_hora × horas (mínimo horas_minimas)."""
        self._validar_horas(horas)
        horas_efectivas = max(horas, self.__horas_minimas)
        return self.precio_hora * horas_efectivas

    def calcular_costo_con_impuesto(self, horas: int, tasa_impuesto: float = 0.19) -> float:
        """Costo incluyendo impuesto de industria y comercio."""
        self._validar_horas(horas)
        base = self.calcular_costo(horas)
        return base * (1 + tasa_impuesto)

    def calcular_costo_con_descuento(self, horas: int, descuento: float = 0.0) -> float:
        """
        Costo con descuento. Asesores experto no aceptan más del 10 % de descuento.
        """
        self._validar_horas(horas)
        if self.__nivel_asesor == "experto" and descuento > 0.10:
            raise ServicioParametroInvalidoError(
                "descuento",
                f"{descuento} (máx. 10 % para asesor experto)"
            )
        if not (0 <= descuento < 1):
            raise ServicioParametroInvalidoError("descuento", descuento)
        base = self.calcular_costo(horas)
        return base * (1 - descuento)

    def validar_parametros(self, horas: int = 1, **kwargs) -> bool:
        """Valida que las horas cumplan el mínimo requerido por nivel."""
        self._validar_horas(horas)
        if horas < self.__horas_minimas:
            raise ServicioParametroInvalidoError(
                "horas",
                f"{horas} (mínimo {self.__horas_minimas} para nivel {self.__nivel_asesor})"
            )
        return True

    # ── Utilidades internas ───────────────────────────────

    @staticmethod
    def _validar_horas(horas: int) -> None:
        if not isinstance(horas, int) or horas <= 0:
            raise ServicioParametroInvalidoError("horas", horas)

    # ── Contrato Entidad ──────────────────────────────────

    def describir(self) -> str:
        return (
            f"{super().describir()} | Área: {self.__area} | "
            f"Nivel: {self.__nivel_asesor.capitalize()} | "
            f"Modalidad: {self.__modalidad.capitalize()} | "
            f"Mín. horas: {self.__horas_minimas}"
        )
