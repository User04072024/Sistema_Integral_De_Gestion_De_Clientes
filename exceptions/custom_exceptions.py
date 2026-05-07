"""
Módulo de excepciones personalizadas para el Sistema Integral
de Gestión de Clientes, Servicios y Reservas - Software FJ.
"""


class SoftwareFJError(Exception):
    """Excepción base del sistema Software FJ."""
    def __init__(self, mensaje: str, codigo: str = "SFJ-000"):
        self.mensaje = mensaje
        self.codigo = codigo
        super().__init__(f"[{codigo}] {mensaje}")


# ──────────────────────────────────────────────
# Excepciones de Cliente
# ──────────────────────────────────────────────

class ClienteError(SoftwareFJError):
    """Base para errores relacionados con clientes."""
    def __init__(self, mensaje: str, codigo: str = "CLI-000"):
        super().__init__(mensaje, codigo)


class ClienteNombreInvalidoError(ClienteError):
    def __init__(self, nombre: str):
        super().__init__(
            f"El nombre '{nombre}' es inválido. Debe tener al menos 2 caracteres y solo letras/espacios.",
            "CLI-001"
        )


class ClienteEmailInvalidoError(ClienteError):
    def __init__(self, email: str):
        super().__init__(
            f"El email '{email}' no tiene un formato válido.",
            "CLI-002"
        )


class ClienteTelefonoInvalidoError(ClienteError):
    def __init__(self, telefono: str):
        super().__init__(
            f"El teléfono '{telefono}' es inválido. Debe contener entre 7 y 15 dígitos.",
            "CLI-003"
        )


class ClienteYaExisteError(ClienteError):
    def __init__(self, email: str):
        super().__init__(
            f"Ya existe un cliente registrado con el email '{email}'.",
            "CLI-004"
        )


class ClienteNoEncontradoError(ClienteError):
    def __init__(self, identificador: str):
        super().__init__(
            f"No se encontró ningún cliente con el identificador '{identificador}'.",
            "CLI-005"
        )


# ──────────────────────────────────────────────
# Excepciones de Servicio
# ──────────────────────────────────────────────

class ServicioError(SoftwareFJError):
    """Base para errores relacionados con servicios."""
    def __init__(self, mensaje: str, codigo: str = "SRV-000"):
        super().__init__(mensaje, codigo)


class ServicioNoDisponibleError(ServicioError):
    def __init__(self, nombre_servicio: str):
        super().__init__(
            f"El servicio '{nombre_servicio}' no está disponible en este momento.",
            "SRV-001"
        )


class ServicioPrecioInvalidoError(ServicioError):
    def __init__(self, precio):
        super().__init__(
            f"El precio '{precio}' es inválido. Debe ser un número positivo.",
            "SRV-002"
        )


class ServicioCapacidadExcedidaError(ServicioError):
    def __init__(self, servicio: str, capacidad: int):
        super().__init__(
            f"El servicio '{servicio}' ha superado su capacidad máxima de {capacidad}.",
            "SRV-003"
        )


class ServicioParametroInvalidoError(ServicioError):
    def __init__(self, parametro: str, valor):
        super().__init__(
            f"El parámetro '{parametro}' tiene un valor inválido: '{valor}'.",
            "SRV-004"
        )


# ──────────────────────────────────────────────
# Excepciones de Reserva
# ──────────────────────────────────────────────

class ReservaError(SoftwareFJError):
    """Base para errores relacionados con reservas."""
    def __init__(self, mensaje: str, codigo: str = "RES-000"):
        super().__init__(mensaje, codigo)


class ReservaDuracionInvalidaError(ReservaError):
    def __init__(self, duracion):
        super().__init__(
            f"La duración '{duracion}' es inválida. Debe ser un número entero positivo (horas).",
            "RES-001"
        )


class ReservaEstadoInvalidoError(ReservaError):
    def __init__(self, estado_actual: str, operacion: str):
        super().__init__(
            f"No se puede realizar '{operacion}' sobre una reserva en estado '{estado_actual}'.",
            "RES-002"
        )


class ReservaNoEncontradaError(ReservaError):
    def __init__(self, id_reserva: str):
        super().__init__(
            f"No se encontró ninguna reserva con el ID '{id_reserva}'.",
            "RES-003"
        )


class ReservaCostoInconsistenteError(ReservaError):
    def __init__(self, detalle: str):
        super().__init__(
            f"Cálculo de costo inconsistente: {detalle}",
            "RES-004"
        )


# ──────────────────────────────────────────────
# Excepciones de Logger
# ──────────────────────────────────────────────

class LoggerError(SoftwareFJError):
    def __init__(self, detalle: str):
        super().__init__(
            f"Error en el sistema de logs: {detalle}",
            "LOG-001"
        )
