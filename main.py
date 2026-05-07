"""
main.py — Sistema Integral de Gestión de Clientes, Servicios y Reservas
Empresa: Software FJ
Curso:   Programación (213023) — UNAD
Equipo:  5 estudiantes

Menú interactivo + 12 operaciones de demostración.
Sin base de datos: toda la gestión se hace en memoria con listas de objetos.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from utils.logger import Logger
from models.cliente import Cliente
from models.reserva import Reserva
from services.reserva_sala import ReservaSala
from services.alquiler_equipo import AlquilerEquipo
from services.asesoria import Asesoria
from exceptions.custom_exceptions import (
    SoftwareFJError,
    ClienteNombreInvalidoError,
    ClienteEmailInvalidoError,
    ClienteTelefonoInvalidoError,
    ServicioNoDisponibleError,
    ServicioParametroInvalidoError,
    ServicioCapacidadExcedidaError,
    ServicioPrecioInvalidoError,
    ReservaDuracionInvalidaError,
    ReservaEstadoInvalidoError,
    ReservaCostoInconsistenteError,
)

# ══════════════════════════════════════════════════════
#  Estado global del sistema (listas en memoria)
# ══════════════════════════════════════════════════════

log = Logger()
clientes:  list = []
servicios: list = []
reservas:  list = []


# ══════════════════════════════════════════════════════
#  Utilidades de interfaz
# ══════════════════════════════════════════════════════

def titulo(texto):
    print(f"\n{'═' * 58}")
    print(f"  {texto}")
    print(f"{'═' * 58}")


def subtitulo(texto):
    print(f"\n{'─' * 58}")
    print(f"  {texto}")
    print(f"{'─' * 58}")


def pausar():
    input("\n  Presione ENTER para continuar...")


def leer_entero(prompt, minimo=1):
    while True:
        try:
            valor = int(input(prompt))
            if valor < minimo:
                print(f"  ⚠  Debe ingresar un número ≥ {minimo}.")
            else:
                return valor
        except ValueError:
            print("  ⚠  Ingrese un número entero válido.")


def seleccionar_de_lista(lista, etiqueta):
    if not lista:
        print(f"  ⚠  No hay {etiqueta} registrados.")
        return None
    print()
    for i, item in enumerate(lista, 1):
        print(f"  [{i}] {item.describir()}")
    idx = leer_entero(f"\n  Seleccione {etiqueta} (número): ", 1)
    if idx > len(lista):
        print("  ⚠  Número fuera de rango.")
        return None
    return lista[idx - 1]


# ══════════════════════════════════════════════════════
#  MÓDULO A — GESTIÓN DE CLIENTES
# ══════════════════════════════════════════════════════

def registrar_cliente():
    subtitulo("Registrar nuevo cliente")
    try:
        nombre   = input("  Nombre completo   : ").strip()
        email    = input("  Correo electrónico: ").strip()
        telefono = input("  Teléfono          : ").strip()
        cliente = Cliente(nombre, email, telefono)
        clientes.append(cliente)
        log.info(f"Cliente registrado: {cliente.describir()}")
        print(f"\n  ✅  Cliente registrado exitosamente.")
        print(f"      {cliente.describir()}")
    except (ClienteNombreInvalidoError,
            ClienteEmailInvalidoError,
            ClienteTelefonoInvalidoError) as e:
        log.error(f"Error al registrar cliente: {e}")
        print(f"\n  ❌  {e}")
    except SoftwareFJError as e:
        log.error(f"Error inesperado: {e}", e)
        print(f"\n  ❌  {e}")
    finally:
        pausar()


def listar_clientes():
    subtitulo("Lista de clientes registrados")
    if not clientes:
        print("  ⚠  No hay clientes registrados aún.")
    else:
        for i, c in enumerate(clientes, 1):
            reservas_c = c.reservas
            print(f"  [{i}] {c.describir()}")
            if reservas_c:
                print(f"       Historial: {len(reservas_c)} reserva(s)")
    pausar()


def buscar_cliente():
    subtitulo("Buscar cliente por nombre o email")
    termino = input("  Ingrese nombre o email: ").strip().lower()
    encontrados = [c for c in clientes
                   if termino in c.nombre.lower() or termino in c.email.lower()]
    if not encontrados:
        print("  ⚠  No se encontraron clientes.")
    else:
        print(f"\n  Se encontraron {len(encontrados)} cliente(s):")
        for c in encontrados:
            print(f"  → {c.describir()}")
    pausar()


def menu_clientes():
    while True:
        titulo("GESTIÓN DE CLIENTES")
        print("  [1] Registrar nuevo cliente")
        print("  [2] Listar todos los clientes")
        print("  [3] Buscar cliente")
        print("  [0] Volver al menú principal")
        opcion = input("\n  Opción: ").strip()
        if opcion == "1":
            registrar_cliente()
        elif opcion == "2":
            listar_clientes()
        elif opcion == "3":
            buscar_cliente()
        elif opcion == "0":
            break
        else:
            print("  ⚠  Opción inválida.")


# ══════════════════════════════════════════════════════
#  MÓDULO B — GESTIÓN DE SERVICIOS
# ══════════════════════════════════════════════════════

def crear_reserva_sala():
    subtitulo("Crear servicio: Reserva de Sala")
    try:
        nombre     = input("  Nombre de la sala        : ").strip() or "Sala de Reuniones"
        capacidad  = leer_entero("  Capacidad (personas)    : ", 1)
        premium    = input("  ¿Es sala premium? (s/n)  : ").strip().lower() == "s"
        disponible = input("  ¿Disponible? (s/n)       : ").strip().lower() != "n"
        precio_str = input("  Precio/hora COP (ENTER=base): ").strip()
        precio = float(precio_str) if precio_str else None
        sala = ReservaSala(nombre=nombre, capacidad=capacidad,
                           es_premium=premium, precio_hora=precio,
                           disponible=disponible)
        servicios.append(sala)
        log.info(f"Servicio creado: {sala.describir()}")
        print(f"\n  ✅  Sala creada.  {sala.describir()}")
    except (ServicioCapacidadExcedidaError, ServicioParametroInvalidoError,
            ServicioPrecioInvalidoError, SoftwareFJError) as e:
        log.error(f"Error al crear sala: {e}")
        print(f"\n  ❌  {e}")
    finally:
        pausar()


def crear_alquiler_equipo():
    subtitulo("Crear servicio: Alquiler de Equipo")
    print("  Tipos válidos: laptop | proyector | tablet | servidor | camara")
    try:
        nombre     = input("  Nombre del equipo         : ").strip() or "Equipo Tecnológico"
        tipo       = input("  Tipo de equipo            : ").strip().lower()
        cantidad   = leer_entero("  Cantidad disponible       : ", 0)
        alta_gama  = input("  ¿Alta gama? (s/n)         : ").strip().lower() == "s"
        disponible = input("  ¿Disponible? (s/n)        : ").strip().lower() != "n"
        precio_str = input("  Precio/hora COP (ENTER=base): ").strip()
        precio = float(precio_str) if precio_str else None
        equipo = AlquilerEquipo(nombre=nombre, tipo_equipo=tipo,
                                cantidad_disponible=cantidad, alta_gama=alta_gama,
                                precio_hora=precio, disponible=disponible)
        servicios.append(equipo)
        log.info(f"Servicio creado: {equipo.describir()}")
        print(f"\n  ✅  Equipo registrado.  {equipo.describir()}")
    except (ServicioParametroInvalidoError, SoftwareFJError) as e:
        log.error(f"Error al crear equipo: {e}")
        print(f"\n  ❌  {e}")
    finally:
        pausar()


def crear_asesoria():
    subtitulo("Crear servicio: Asesoría Especializada")
    print("  Niveles: junior | senior | experto")
    print("  Modalidades: presencial | virtual")
    try:
        nombre     = input("  Nombre/título            : ").strip() or "Asesoría Especializada"
        area       = input("  Área temática            : ").strip() or "Tecnología"
        nivel      = input("  Nivel del asesor         : ").strip().lower()
        modalidad  = input("  Modalidad                : ").strip().lower()
        disponible = input("  ¿Disponible? (s/n)       : ").strip().lower() != "n"
        precio_str = input("  Precio/hora COP (ENTER=base): ").strip()
        precio = float(precio_str) if precio_str else None
        asesoria = Asesoria(nombre=nombre, area=area, nivel_asesor=nivel,
                            modalidad=modalidad, precio_hora=precio,
                            disponible=disponible)
        servicios.append(asesoria)
        log.info(f"Servicio creado: {asesoria.describir()}")
        print(f"\n  ✅  Asesoría creada.  {asesoria.describir()}")
    except (ServicioParametroInvalidoError, SoftwareFJError) as e:
        log.error(f"Error al crear asesoría: {e}")
        print(f"\n  ❌  {e}")
    finally:
        pausar()


def listar_servicios():
    subtitulo("Lista de servicios registrados")
    if not servicios:
        print("  ⚠  No hay servicios registrados aún.")
    else:
        for i, s in enumerate(servicios, 1):
            print(f"  [{i}] {s.describir()}")
    pausar()


def calcular_costos_servicio():
    subtitulo("Calcular costos de un servicio")
    srv = seleccionar_de_lista(servicios, "servicio")
    if not srv:
        pausar()
        return
    try:
        horas   = leer_entero("  Horas a calcular: ", 1)
        base    = srv.calcular_costo(horas)
        con_iva = srv.calcular_costo_con_impuesto(horas)
        con_dto = srv.calcular_costo_con_descuento(horas, 0.10)
        print(f"\n  Servicio  : {srv.nombre}")
        print(f"  Horas     : {horas}")
        print(f"  Costo base: ${base:>12,.2f} COP")
        print(f"  Con IVA   : ${con_iva:>12,.2f} COP")
        print(f"  Desc. 10% : ${con_dto:>12,.2f} COP")
        log.info(f"Cálculo — {srv.nombre} | {horas}h | ${base:,.2f}")
    except SoftwareFJError as e:
        log.error(f"Error en cálculo: {e}")
        print(f"\n  ❌  {e}")
    finally:
        pausar()


def menu_servicios():
    while True:
        titulo("GESTIÓN DE SERVICIOS")
        print("  [1] Crear — Reserva de Sala")
        print("  [2] Crear — Alquiler de Equipo")
        print("  [3] Crear — Asesoría Especializada")
        print("  [4] Listar todos los servicios")
        print("  [5] Calcular costos de un servicio")
        print("  [0] Volver al menú principal")
        opcion = input("\n  Opción: ").strip()
        if opcion == "1":
            crear_reserva_sala()
        elif opcion == "2":
            crear_alquiler_equipo()
        elif opcion == "3":
            crear_asesoria()
        elif opcion == "4":
            listar_servicios()
        elif opcion == "5":
            calcular_costos_servicio()
        elif opcion == "0":
            break
        else:
            print("  ⚠  Opción inválida.")


# ══════════════════════════════════════════════════════
#  MÓDULO C — GESTIÓN DE RESERVAS
# ══════════════════════════════════════════════════════

def crear_reserva():
    subtitulo("Crear nueva reserva")
    try:
        print("\n  — Seleccione el CLIENTE —")
        cliente = seleccionar_de_lista(clientes, "cliente")
        if not cliente:
            pausar()
            return
        print("\n  — Seleccione el SERVICIO —")
        servicio = seleccionar_de_lista(servicios, "servicio")
        if not servicio:
            pausar()
            return
        duracion  = leer_entero("  Duración en horas (entero > 0): ", 1)
        desc_str  = input("  Descuento 0-99% (ENTER = 0)    : ").strip()
        descuento = float(desc_str) / 100 if desc_str else 0.0
        if not (0.0 <= descuento < 1.0):
            print("  ⚠  Descuento fuera de rango, se usará 0%.")
            descuento = 0.0
        aplicar_iva = input("  ¿Aplicar IVA 19%? (s/n)        : ").strip().lower() != "n"
        reserva = Reserva(cliente=cliente, servicio=servicio,
                          duracion_horas=duracion, descuento=descuento,
                          aplicar_impuesto=aplicar_iva)
        reservas.append(reserva)
        log.info(f"Reserva creada: {reserva.describir()}")
        print(f"\n  ✅  Reserva creada en estado PENDIENTE.")
        print(f"      {reserva.describir()}")
    except ReservaDuracionInvalidaError as e:
        log.error(f"Duración inválida: {e}")
        print(f"\n  ❌  {e}")
    except ServicioNoDisponibleError as e:
        log.error(f"Servicio no disponible: {e}")
        print(f"\n  ❌  {e}")
    except (TypeError, SoftwareFJError) as e:
        log.error(f"Error al crear reserva: {e}", e)
        print(f"\n  ❌  {e}")
    finally:
        pausar()


def confirmar_reserva():
    subtitulo("Confirmar reserva (PENDIENTE → CONFIRMADA)")
    pendientes = [r for r in reservas if r.estado == "pendiente"]
    if not pendientes:
        print("  ⚠  No hay reservas en estado PENDIENTE.")
        pausar()
        return
    try:
        reserva = seleccionar_de_lista(pendientes, "reserva pendiente")
        if not reserva:
            pausar()
            return
        reserva.confirmar()
        log.info(f"Reserva confirmada: {reserva.id_reserva}")
        print(f"\n  ✅  Reserva confirmada.")
        print(f"      {reserva.describir()}")
    except (ReservaEstadoInvalidoError, SoftwareFJError) as e:
        log.error(f"Error al confirmar: {e}")
        print(f"\n  ❌  {e}")
    finally:
        pausar()


def procesar_reserva():
    subtitulo("Procesar reserva (CONFIRMADA → PROCESADA)")
    confirmadas = [r for r in reservas if r.estado == "confirmada"]
    if not confirmadas:
        print("  ⚠  No hay reservas en estado CONFIRMADA.")
        pausar()
        return
    try:
        reserva = seleccionar_de_lista(confirmadas, "reserva confirmada")
        if not reserva:
            pausar()
            return
        costo = reserva.procesar()
        log.info(f"Reserva procesada: {reserva.id_reserva} | ${costo:,.2f}")
        print(f"\n  ✅  Reserva procesada.")
        print(f"      Costo total: ${costo:,.2f} COP")
        print(f"      {reserva.describir()}")
    except (ReservaEstadoInvalidoError, ReservaCostoInconsistenteError,
            SoftwareFJError) as e:
        log.error(f"Error al procesar: {e}")
        print(f"\n  ❌  {e}")
    finally:
        pausar()


def cancelar_reserva():
    subtitulo("Cancelar reserva")
    cancelables = [r for r in reservas if r.estado in ("pendiente", "confirmada")]
    if not cancelables:
        print("  ⚠  No hay reservas que se puedan cancelar.")
        pausar()
        return
    try:
        reserva = seleccionar_de_lista(cancelables, "reserva")
        if not reserva:
            pausar()
            return
        confirmar = input(f"\n  ¿Cancelar la reserva {reserva.id_reserva}? (s/n): ").strip().lower()
        if confirmar != "s":
            print("  Cancelación abortada.")
            pausar()
            return
        reserva.cancelar()
        log.info(f"Reserva cancelada: {reserva.id_reserva}")
        print(f"\n  ✅  Reserva cancelada.")
        print(f"      {reserva.describir()}")
    except (ReservaEstadoInvalidoError, SoftwareFJError) as e:
        log.error(f"Error al cancelar: {e}")
        print(f"\n  ❌  {e}")
    finally:
        pausar()


def listar_reservas():
    subtitulo("Lista de todas las reservas")
    if not reservas:
        print("  ⚠  No hay reservas registradas aún.")
    else:
        iconos = {"pendiente": "🟡", "confirmada": "🔵",
                  "procesada": "🟢", "cancelada": "🔴"}
        for i, r in enumerate(reservas, 1):
            icono = iconos.get(r.estado, "⚪")
            print(f"  [{i}] {icono} {r.describir()}")
    pausar()


def menu_reservas():
    while True:
        titulo("GESTIÓN DE RESERVAS")
        print("  [1] Crear nueva reserva          (→ PENDIENTE)")
        print("  [2] Confirmar reserva             (→ CONFIRMADA)")
        print("  [3] Procesar reserva              (→ PROCESADA)")
        print("  [4] Cancelar reserva")
        print("  [5] Listar todas las reservas")
        print("  [0] Volver al menú principal")
        opcion = input("\n  Opción: ").strip()
        if opcion == "1":
            crear_reserva()
        elif opcion == "2":
            confirmar_reserva()
        elif opcion == "3":
            procesar_reserva()
        elif opcion == "4":
            cancelar_reserva()
        elif opcion == "5":
            listar_reservas()
        elif opcion == "0":
            break
        else:
            print("  ⚠  Opción inválida.")


# ══════════════════════════════════════════════════════
#  MÓDULO D — DEMO (12 operaciones automatizadas)
# ══════════════════════════════════════════════════════

def encabezado(texto):
    log.separador(texto)


def op1_cliente_valido():
    encabezado("OP-01 | Registro de cliente válido")
    try:
        c = Cliente("Ana Lucía Martínez", "ana.martinez@softwarefj.com", "+57 310 4567890")
        log.info(f"Cliente creado: {c.describir()}")
        log.info(f"  Validación interna: {c.validar()}")
        clientes.append(c)
        return c
    except SoftwareFJError as e:
        log.error(f"Error en OP-01: {e}", e)
    finally:
        log.info("OP-01 finalizada.")


def op2_clientes_invalidos():
    encabezado("OP-02 | Clientes con datos inválidos")
    casos = [
        ("A", "ok@mail.com", "3101234567"),
        ("Pedro Pérez", "correo-sin-arroba", "3101234567"),
        ("Pedro Pérez", "pedro@mail.com", "123"),
        ("12345 nombre", "x@x.com", "3001234567"),
    ]
    for nombre, email, telefono in casos:
        try:
            c = Cliente(nombre, email, telefono)
            log.advertencia(f"Se esperaba error pero se creó: {c.describir()}")
        except (ClienteNombreInvalidoError, ClienteEmailInvalidoError,
                ClienteTelefonoInvalidoError) as e:
            log.error(f"Capturado correctamente: {e}")
        except SoftwareFJError as e:
            log.error(f"Error genérico: {e}", e)
        finally:
            log.info("  Intento procesado (finally).")


def op3_servicios_validos():
    encabezado("OP-03 | Creación de servicios válidos")
    svcs = []
    try:
        items = [
            ReservaSala("Sala Innovación", capacidad=15, es_premium=False),
            ReservaSala("Sala Directivos", capacidad=8, es_premium=True),
            AlquilerEquipo("Laptop HP Elite", tipo_equipo="laptop",
                           cantidad_disponible=10, alta_gama=True),
            Asesoria("Asesoría Ciberseguridad", area="Seguridad",
                     nivel_asesor="experto", modalidad="presencial"),
        ]
        for s in items:
            log.info(f"Servicio: {s.describir()}")
            svcs.append(s)
            servicios.append(s)
    except SoftwareFJError as e:
        log.error(f"Error: {e}", e)
    else:
        log.info("Todos los servicios creados (else).")
    finally:
        log.info("OP-03 finalizada.")
    return svcs


def op4_servicios_invalidos():
    encabezado("OP-04 | Servicios con parámetros inválidos")
    try:
        ReservaSala("Sala Error", capacidad=5, precio_hora=-1000)
    except ServicioPrecioInvalidoError as e:
        log.error(f"4a Precio inválido: {e}")
    try:
        ReservaSala("Sala Gigante", capacidad=999)
    except ServicioCapacidadExcedidaError as e:
        log.error(f"4b Capacidad excedida: {e}")
    try:
        AlquilerEquipo("Equipo Misterio", tipo_equipo="submarino")
    except ServicioParametroInvalidoError as e:
        log.error(f"4c Tipo inválido: {e}")
    try:
        Asesoria("Asesoría VIP", nivel_asesor="dios")
    except ServicioParametroInvalidoError as e:
        log.error(f"4d Nivel inválido: {e}")
    log.info("OP-04 finalizada.")


def op5_calculo_costos(svcs):
    encabezado("OP-05 | Cálculo polimórfico de costos")
    if not svcs:
        log.advertencia("Sin servicios para OP-05."); return
    try:
        for srv in svcs:
            h = 3
            b = srv.calcular_costo(h)
            v = srv.calcular_costo_con_impuesto(h)
            d = srv.calcular_costo_con_descuento(h, 0.10)
            log.info(f"  {srv.nombre:<35} | Base:${b:>10,.2f} | IVA:${v:>10,.2f} | -10%:${d:>10,.2f}")
    except SoftwareFJError as e:
        log.error(f"Error: {e}", e)
    finally:
        log.info("OP-05 finalizada.")


def op6_reserva_exitosa(cliente, svcs):
    encabezado("OP-06 | Reserva exitosa — flujo completo")
    if not cliente or not svcs:
        log.advertencia("Datos insuficientes."); return None
    reserva = None
    try:
        sala = svcs[0]
        sala.validar_parametros(personas=10)
        reserva = Reserva(cliente, sala, duracion_horas=4, descuento=0.05,
                          aplicar_impuesto=True)
        log.info(f"Creada: {reserva.describir()}")
        reserva.confirmar()
        log.info(f"Confirmada: {reserva.estado.upper()}")
        costo = reserva.procesar()
        log.info(f"Procesada — Costo: ${costo:,.2f}")
        reservas.append(reserva)
    except SoftwareFJError as e:
        log.error(f"Error en OP-06: {e}", e)
    else:
        log.info("Reserva completada sin errores (else).")
    finally:
        log.info("OP-06 finalizada.")
    return reserva


def op7_reserva_duracion_invalida(cliente, svcs):
    encabezado("OP-07 | Reserva con duración inválida")
    if not cliente or not svcs:
        log.advertencia("Datos insuficientes."); return
    try:
        Reserva(cliente, svcs[0], duracion_horas=-5)
    except ReservaDuracionInvalidaError as e:
        log.error(f"Capturado: {e}")
    except SoftwareFJError as e:
        log.error(f"Error: {e}", e)
    finally:
        log.info("OP-07 finalizada.")


def op8_servicio_no_disponible(cliente):
    encabezado("OP-08 | Reserva sobre servicio no disponible")
    if not cliente:
        log.advertencia("Sin cliente."); return
    try:
        sala = ReservaSala("Sala en Mantenimiento", capacidad=5, disponible=False)
        log.info(f"Servicio: {sala.describir()}")
        Reserva(cliente, sala, duracion_horas=2)
    except ServicioNoDisponibleError as e:
        log.error(f"Capturado: {e}")
    except SoftwareFJError as e:
        log.error(f"Error: {e}", e)
    finally:
        log.info("OP-08 finalizada.")


def op9_estado_invalido(reserva_proc):
    encabezado("OP-09 | Cancelar reserva ya procesada")
    if not reserva_proc:
        log.advertencia("Sin reserva procesada."); return
    try:
        reserva_proc.cancelar()
    except ReservaEstadoInvalidoError as e:
        log.error(f"Capturado: {e}")
    except SoftwareFJError as e:
        log.error(f"Error: {e}", e)
    finally:
        log.info("OP-09 finalizada.")


def op10_encadenamiento(cliente, svcs):
    encabezado("OP-10 | Encadenamiento de excepciones (raise ... from ...)")
    if not cliente or not svcs:
        log.advertencia("Datos insuficientes."); return
    try:
        asesorias = [s for s in svcs if isinstance(s, Asesoria)]
        if not asesorias:
            raise ValueError("No hay asesorías disponibles.")
        srv = asesorias[0]
        try:
            srv.validar_parametros(horas=1)
        except ServicioParametroInvalidoError as causa:
            raise ReservaCostoInconsistenteError(
                f"Parámetros inválidos: {causa.mensaje}"
            ) from causa
    except ReservaCostoInconsistenteError as e:
        log.error(f"Excepción encadenada: {e}")
        if e.__cause__:
            log.error(f"  Causa original: {e.__cause__}")
    except Exception as e:
        log.error(f"Error genérico: {e}", e)
    finally:
        log.info("OP-10 finalizada.")


def op11_stock_insuficiente(cliente):
    encabezado("OP-11 | Alquiler con stock insuficiente")
    if not cliente:
        log.advertencia("Sin cliente."); return
    try:
        equipo = AlquilerEquipo("Tablet Samsung", tipo_equipo="tablet",
                                cantidad_disponible=2)
        log.info(f"Equipo: {equipo.describir()}")
        equipo.validar_parametros(cantidad=10)
    except ServicioNoDisponibleError as e:
        log.error(f"Capturado: {e}")
    except SoftwareFJError as e:
        log.error(f"Error: {e}", e)
    finally:
        log.info("OP-11 finalizada.")


def op12_asesoria_virtual(cliente):
    encabezado("OP-12 | Asesoría senior virtual con descuento")
    if not cliente:
        log.advertencia("Sin cliente."); return
    try:
        asesoria = Asesoria("Consultoría Cloud", area="Infraestructura",
                            nivel_asesor="senior", modalidad="virtual")
        log.info(f"Servicio: {asesoria.describir()}")
        r = Reserva(cliente, asesoria, duracion_horas=3,
                    descuento=0.08, aplicar_impuesto=True)
        r.confirmar()
        costo = r.procesar()
        log.info(f"Procesada — Costo: ${costo:,.2f}")
        reservas.append(r)
    except SoftwareFJError as e:
        log.error(f"Error en OP-12: {e}", e)
    else:
        log.info("OP-12 completada sin errores (else).")
    finally:
        log.info("OP-12 finalizada.")


def ejecutar_demo():
    titulo("MODO DEMOSTRACIÓN — 12 Operaciones Automáticas")
    print("\n  Ejecuta operaciones predefinidas (válidas e inválidas).")
    print("  Los datos cargados quedarán disponibles en los menús.\n")
    if input("  ¿Continuar? (s/n): ").strip().lower() != "s":
        return
    cliente = op1_cliente_valido()
    op2_clientes_invalidos()
    svcs = op3_servicios_validos()
    op4_servicios_invalidos()
    op5_calculo_costos(svcs)
    reserva = op6_reserva_exitosa(cliente, svcs)
    op7_reserva_duracion_invalida(cliente, svcs)
    op8_servicio_no_disponible(cliente)
    op9_estado_invalido(reserva)
    op10_encadenamiento(cliente, svcs)
    op11_stock_insuficiente(cliente)
    op12_asesoria_virtual(cliente)
    print(f"\n{'═' * 58}")
    print("  ✅  Demo completada. Revise logs/eventos.log")
    print(f"{'═' * 58}")
    pausar()


# ══════════════════════════════════════════════════════
#  RESUMEN DEL SISTEMA
# ══════════════════════════════════════════════════════

def mostrar_resumen():
    titulo("RESUMEN DEL SISTEMA")
    pendientes  = sum(1 for r in reservas if r.estado == "pendiente")
    confirmadas = sum(1 for r in reservas if r.estado == "confirmada")
    procesadas  = sum(1 for r in reservas if r.estado == "procesada")
    canceladas  = sum(1 for r in reservas if r.estado == "cancelada")
    ingresos    = sum(r.costo_total for r in reservas if r.estado == "procesada")
    print(f"\n  Clientes registrados  : {len(clientes)}")
    print(f"  Servicios disponibles : {len(servicios)}")
    print(f"  Total de reservas     : {len(reservas)}")
    print(f"    🟡 Pendientes        : {pendientes}")
    print(f"    🔵 Confirmadas       : {confirmadas}")
    print(f"    🟢 Procesadas        : {procesadas}")
    print(f"    🔴 Canceladas        : {canceladas}")
    print(f"\n  💰 Ingresos procesados : ${ingresos:,.2f} COP")
    print(f"\n  📋 Logs guardados en   : logs/eventos.log")
    log.info(f"Resumen — Clientes:{len(clientes)} | Servicios:{len(servicios)} | Reservas:{len(reservas)} | Ingresos:${ingresos:,.2f}")
    pausar()


# ══════════════════════════════════════════════════════
#  MENÚ PRINCIPAL
# ══════════════════════════════════════════════════════

def main():
    while True:
        titulo("SISTEMA INTEGRAL DE GESTIÓN — Software FJ")
        print(f"  Clientes: {len(clientes)}  |  Servicios: {len(servicios)}  |  Reservas: {len(reservas)}")
        print()
        print("  [1] Gestión de Clientes")
        print("  [2] Gestión de Servicios")
        print("  [3] Gestión de Reservas")
        print("  [4] Resumen del sistema")
        print("  [5] Ejecutar Demo (12 operaciones automáticas)")
        print("  [0] Salir")
        opcion = input("\n  Opción: ").strip()
        if opcion == "1":
            menu_clientes()
        elif opcion == "2":
            menu_servicios()
        elif opcion == "3":
            menu_reservas()
        elif opcion == "4":
            mostrar_resumen()
        elif opcion == "5":
            ejecutar_demo()
        elif opcion == "0":
            log.info("Sistema cerrado por el usuario.")
            print("\n  👋  ¡Hasta luego!\n")
            sys.exit(0)
        else:
            print("  ⚠  Opción inválida.")


if __name__ == "__main__":
    main()
