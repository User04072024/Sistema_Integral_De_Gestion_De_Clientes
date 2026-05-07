"""
Módulo de la clase Cliente con validaciones robustas
y encapsulación de datos personales.
"""

import re
from models.entidad import Entidad
from exceptions.custom_exceptions import (
    ClienteNombreInvalidoError,
    ClienteEmailInvalidoError,
    ClienteTelefonoInvalidoError,
)


class Cliente(Entidad):
    """
    Representa un cliente de Software FJ.
    Hereda de Entidad e implementa encapsulación y validaciones estrictas.
    """

    _contador_clientes: int = 0
    _PATRON_EMAIL = re.compile(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$")
    _PATRON_TELEFONO = re.compile(r"^\+?[\d\s\-]{7,15}$")
    _PATRON_NOMBRE = re.compile(r"^[A-Za-záéíóúÁÉÍÓÚñÑ\s]{2,60}$")

    def __init__(self, nombre: str, email: str, telefono: str):
        """
        Crea un nuevo cliente validando todos sus datos.

        Args:
            nombre:   Nombre completo (solo letras y espacios, 2-60 chars).
            email:    Dirección de correo electrónico válida.
            telefono: Número telefónico (7-15 dígitos, puede incluir +, - y espacios).

        Raises:
            ClienteNombreInvalidoError: Si el nombre no cumple el formato.
            ClienteEmailInvalidoError:  Si el email no cumple el formato.
            ClienteTelefonoInvalidoError: Si el teléfono no cumple el formato.
        """
        # Validar antes de llamar al padre
        self._validar_nombre(nombre)
        self._validar_email(email)
        self._validar_telefono(telefono)

        super().__init__(nombre)

        Cliente._contador_clientes += 1
        self.__id_cliente: str = f"CLI-{Cliente._contador_clientes:04d}"
        self.__email: str = email.lower().strip()
        self.__telefono: str = telefono.strip()
        self.__activo: bool = True
        self.__reservas: list = []

    # ── Validaciones estáticas ────────────────────────────

    @staticmethod
    def _validar_nombre(nombre: str) -> None:
        if not nombre or not Cliente._PATRON_NOMBRE.match(nombre.strip()):
            raise ClienteNombreInvalidoError(nombre)

    @staticmethod
    def _validar_email(email: str) -> None:
        if not email or not Cliente._PATRON_EMAIL.match(email.strip()):
            raise ClienteEmailInvalidoError(email)

    @staticmethod
    def _validar_telefono(telefono: str) -> None:
        digitos = re.sub(r"[\s\-\+]", "", telefono)
        if not digitos.isdigit() or not (7 <= len(digitos) <= 15):
            raise ClienteTelefonoInvalidoError(telefono)

    # ── Propiedades ───────────────────────────────────────

    @property
    def id_cliente(self) -> str:
        return self.__id_cliente

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, nuevo_email: str) -> None:
        self._validar_email(nuevo_email)
        self.__email = nuevo_email.lower().strip()

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, nuevo_telefono: str) -> None:
        self._validar_telefono(nuevo_telefono)
        self.__telefono = nuevo_telefono.strip()

    @property
    def activo(self) -> bool:
        return self.__activo

    @property
    def reservas(self) -> list:
        return list(self.__reservas)  # copia defensiva

    # ── Métodos de negocio ────────────────────────────────

    def agregar_reserva(self, reserva) -> None:
        """Asocia una reserva al historial del cliente."""
        self.__reservas.append(reserva)

    def desactivar(self) -> None:
        """Marca el cliente como inactivo."""
        self.__activo = False

    # ── Contrato Entidad ──────────────────────────────────

    def describir(self) -> str:
        estado = "Activo" if self.__activo else "Inactivo"
        return (
            f"Cliente [{self.__id_cliente}] | {self.nombre} | "
            f"Email: {self.__email} | Tel: {self.__telefono} | Estado: {estado}"
        )

    def validar(self) -> bool:
        try:
            self._validar_nombre(self.nombre)
            self._validar_email(self.__email)
            self._validar_telefono(self.__telefono)
            return True
        except Exception:
            return False
