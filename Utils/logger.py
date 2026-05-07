"""
Módulo utilitario de registro de eventos y errores (Logger).
Todos los eventos relevantes y errores se escriben en logs/eventos.log.
"""

import os
import traceback
from datetime import datetime

from exceptions.custom_exceptions import LoggerError


class Logger:
    """
    Clase utilitaria para registrar eventos y errores en archivo de logs.
    Implementa patrón Singleton para garantizar una única instancia.
    """

    _instancia = None
    _ruta_log: str = os.path.join("logs", "eventos.log")

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia

    def _inicializar(self) -> None:
        """Crea el directorio y archivo de logs si no existen."""
        try:
            os.makedirs("logs", exist_ok=True)
            # Escribe encabezado si el archivo es nuevo
            if not os.path.exists(self._ruta_log):
                with open(self._ruta_log, "w", encoding="utf-8") as f:
                    f.write("=" * 70 + "\n")
                    f.write("   SISTEMA DE LOGS - Software FJ\n")
                    f.write(f"   Iniciado: {self._timestamp()}\n")
                    f.write("=" * 70 + "\n\n")
        except OSError as e:
            raise LoggerError(f"No se pudo inicializar el archivo de logs: {e}") from e

    @staticmethod
    def _timestamp() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _escribir(self, nivel: str, mensaje: str) -> None:
        """Escribe una línea en el archivo de logs."""
        try:
            with open(self._ruta_log, "a", encoding="utf-8") as f:
                f.write(f"[{self._timestamp()}] [{nivel}] {mensaje}\n")
        except OSError as e:
            # Si no se puede escribir en el log, al menos se imprime
            print(f"[LOGGER-FALLBACK] No se pudo escribir en log: {e}")

    def info(self, mensaje: str) -> None:
        """Registra un evento informativo."""
        self._escribir("INFO ", mensaje)
        print(f"  ✅ INFO  | {mensaje}")

    def advertencia(self, mensaje: str) -> None:
        """Registra una advertencia."""
        self._escribir("WARN ", mensaje)
        print(f"  ⚠️  WARN  | {mensaje}")

    def error(self, mensaje: str, excepcion: Exception = None) -> None:
        """Registra un error, opcionalmente con el traceback completo."""
        self._escribir("ERROR", mensaje)
        print(f"  ❌ ERROR | {mensaje}")
        if excepcion:
            tb = traceback.format_exc()
            self._escribir("TRACE", tb.strip())

    def separador(self, titulo: str = "") -> None:
        """Escribe un separador visual en el log."""
        linea = f"─── {titulo} " + "─" * max(0, 50 - len(titulo))
        self._escribir("─────", linea)
        print(f"\n{'─' * 55}")
        if titulo:
            print(f"  {titulo}")
        print(f"{'─' * 55}")
