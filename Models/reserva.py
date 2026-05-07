"""
Módulo de la clase Reserva.
Integra cliente, servicio, duración y estado.
Implementa confirmación, cancelación y procesamiento
con manejo robusto de excepciones.
"""

from datetime import datetime
from models.entidad import Entidad
from models.cliente import Cliente
from models.servicio import Servicio
from exceptions.custom_exceptions import (
    ReservaDuracionInvalidaError,
    ReservaEstadoInvalidoError,
    ReservaCostoInconsistenteError,
    ServicioNoDisponibleError,
)

ESTADOS = {"pendiente", "confirmada", "cancelada", "procesada"}


class Reserva(Entidad):
    """
    Representa una reserva de un servicio por parte de un cliente.
    Gestiona el ciclo de vida: pendiente → confirmada → procesada / cancelada.
    """

    _contador_reservas: int = 0

    def __init__(
        self,
        cliente: Cliente,
        servicio: Servicio,
        duracion_horas: int,
        descuento: float = 0.0,
        aplicar_impuesto: bool = True,
    ):
        """
        Args:
            cliente:          Cliente que realiza la reserva.
            servicio:         Servicio a reservar.
            duracion_horas:   Duración en horas (entero positivo).
            descuento:        Descuento porcentual (0.0 – 0.99).
            aplicar_impuesto: Si True, incluye IVA del 19 %.

        Raises:
            TypeError:                   Si cliente o servicio no son instancias válidas.
            ReservaDuracionInvalidaError: Si duracion_horas no es entero positivo.
            ServicioNoDisponibleError:    Si el servicio no está disponible.
        """
        if not isinstance(cliente, Cliente):
            raise TypeError("El parámetro 'cliente' debe ser una instancia de Cliente.")
        if not isinstance(servicio, Servicio):
            raise TypeError("El parámetro 'servicio' debe ser una instancia de Servicio.")
        if not isinstance(duracion_horas, int) or duracion_horas <= 0:
            raise ReservaDuracionInvalidaError(duracion_horas)

        # Verificar disponibilidad (puede lanzar ServicioNoDisponibleError)
        servicio.verificar_disponibilidad()

        super().__init__(f"Reserva de {servicio.nombre}")

        Reserva._contador_reservas += 1
        self.__id_reserva: str = f"RES-{Reserva._contador_reservas:05d}"
        self.__cliente: Cliente = cliente
        self.__servicio: Servicio = servicio
        self.__duracion_horas: int = duracion_horas
        self.__descuento: float = descuento
        self.__aplicar_impuesto: bool = aplicar_impuesto
        self.__estado: str = "pendiente"
        self.__fecha_reserva: datetime = datetime.now()
        self.__fecha_procesamiento: datetime = None
        self.__costo_total: float = 0.0

        # Asociar reserva al cliente
        cliente.agregar_reserva(self)

    # ── Propiedades ───────────────────────────────────────

    @property
    def id_reserva(self) -> str:
        return self.__id_reserva

    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    @property
    def servicio(self) -> Servicio:
        return self.__servicio

    @property
    def duracion_horas(self) -> int:
        return self.__duracion_horas

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def costo_total(self) -> float:
        return self.__costo_total

    @property
    def fecha_reserva(self) -> datetime:
        return self.__fecha_reserva

    # ── Métodos del ciclo de vida ─────────────────────────

    def confirmar(self) -> None:
        """
        Confirma la reserva si está en estado 'pendiente'.

        Raises:
            ReservaEstadoInvalidoError: Si el estado no permite confirmación.
        """
        if self.__estado != "pendiente":
            raise ReservaEstadoInvalidoError(self.__estado, "confirmar")
        self.__estado = "confirmada"

    def cancelar(self) -> None:
        """
        Cancela la reserva si no ha sido ya procesada.

        Raises:
            ReservaEstadoInvalidoError: Si el estado no permite cancelación.
        """
        if self.__estado == "procesada":
            raise ReservaEstadoInvalidoError(self.__estado, "cancelar")
        if self.__estado == "cancelada":
            raise ReservaEstadoInvalidoError(self.__estado, "cancelar (ya cancelada)")
        self.__estado = "cancelada"

    def procesar(self) -> float:
        """
        Procesa la reserva: calcula el costo total y la marca como procesada.

        Returns:
            Costo total calculado.

        Raises:
            ReservaEstadoInvalidoError:      Si no está confirmada.
            ReservaCostoInconsistenteError:  Si el costo calculado es inválido.
        """
        if self.__estado != "confirmada":
            raise ReservaEstadoInvalidoError(self.__estado, "procesar")

        try:
            if self.__aplicar_impuesto and self.__descuento > 0:
                # Primero descuento, luego impuesto
                costo_desc = self.__servicio.calcular_costo_con_descuento(
                    self.__duracion_horas, self.__descuento
                )
                costo = costo_desc * 1.19
            elif self.__aplicar_impuesto:
                costo = self.__servicio.calcular_costo_con_impuesto(self.__duracion_horas)
            elif self.__descuento > 0:
                costo = self.__servicio.calcular_costo_con_descuento(
                    self.__duracion_horas, self.__descuento
                )
            else:
                costo = self.__servicio.calcular_costo(self.__duracion_horas)

            if costo <= 0:
                raise ReservaCostoInconsistenteError(
                    f"El costo calculado fue {costo}, esperado > 0"
                )

            self.__costo_total = costo
            self.__estado = "procesada"
            self.__fecha_procesamiento = datetime.now()
            return self.__costo_total

        except (ReservaCostoInconsistenteError, ReservaEstadoInvalidoError):
            raise
        except Exception as e:
            raise ReservaCostoInconsistenteError(
                f"Error inesperado al calcular el costo: {e}"
            ) from e

    # ── Contrato Entidad ──────────────────────────────────

    def describir(self) -> str:
        costo_str = f"${self.__costo_total:,.2f}" if self.__costo_total else "No calculado"
        proc = (
            self.__fecha_procesamiento.strftime("%Y-%m-%d %H:%M:%S")
            if self.__fecha_procesamiento else "—"
        )
        return (
            f"Reserva [{self.__id_reserva}] | Estado: {self.__estado.upper()} | "
            f"Cliente: {self.__cliente.nombre} | Servicio: {self.__servicio.nombre} | "
            f"Duración: {self.__duracion_horas}h | Costo: {costo_str} | "
            f"Procesado: {proc}"
        )

    def validar(self) -> bool:
        return (
            isinstance(self.__cliente, Cliente)
            and isinstance(self.__servicio, Servicio)
            and self.__duracion_horas > 0
            and self.__estado in ESTADOS
        )
