"""
Módulo de la clase Cliente.
"""

import re
from models.entidad import Entidad
from exceptions.custom_exceptions import (
    ClienteNombreInvalidoError,
    ClienteEmailInvalidoError,
    ClienteTelefonoInvalidoError,
)

#datos del cliente
class Cliente(Entidad):

    _contador_clientes = 0
    _PATRON_EMAIL = re.compile(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$")
    _PATRON_TELEFONO = re.compile(r"^\+?[\d\s\-]{7,15}$")
    _PATRON_NOMBRE = re.compile(r"^[A-Za-záéíóúÁÉÍÓÚñÑ\s]{2,60}$")

    def __init__(self, nombre: str, email: str, telefono: str):
        self._validar_nombre(nombre)
        self._validar_email(email)
        self._validar_telefono(telefono)

        super().__init__(nombre)

        Cliente._contador_clientes += 1
        self.__id_cliente = f"CLI-{Cliente._contador_clientes:04d}"
        self.__email = email.lower().strip()
        self.__telefono = telefono.strip()
        self.__activo = True
        self.__reservas = []

    # Validaciones

    @staticmethod
    def _validar_nombre(nombre: str):
        if not nombre or not Cliente._PATRON_NOMBRE.match(nombre.strip()):
            raise ClienteNombreInvalidoError(nombre)

    @staticmethod
    def _validar_email(email: str):
        if not email or not Cliente._PATRON_EMAIL.match(email.strip()):
            raise ClienteEmailInvalidoError(email)

    @staticmethod
    def _validar_telefono(telefono: str):
        digitos = re.sub(r"[\s\-\+]", "", telefono)
        if not digitos.isdigit() or not (7 <= len(digitos) <= 15):
            raise ClienteTelefonoInvalidoError(telefono)

    # Propiedades

    @property
    def id_cliente(self):
        return self.__id_cliente

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, nuevo_email: str):
        self._validar_email(nuevo_email)
        self.__email = nuevo_email.lower().strip()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, nuevo_telefono: str):
        self._validar_telefono(nuevo_telefono)
        self.__telefono = nuevo_telefono.strip()

    @property
    def activo(self):
        return self.__activo

    @property
    def reservas(self):
        return list(self.__reservas)

    # Métodos

    def agregar_reserva(self, reserva):
        self.__reservas.append(reserva)

    def desactivar(self):
        self.__activo = False

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
