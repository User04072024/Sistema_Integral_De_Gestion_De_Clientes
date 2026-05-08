"""
Ejercicio: Sistema de Gestión de Clientes, Servicios y Reservas. Empresa: Software FJ
Curso: Programación (213023) UNAD
Grupo:
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

log = Logger()
clientes = []
servicios = []
reservas = []


def pausar():
    input("\nPresione ENTER para continuar...")


def leer_entero(prompt, minimo=1):
    while True:
        try:
            valor = int(input(prompt))
            if valor < minimo:
                print(f"Debe ingresar un número >= {minimo}.")
            else:
                return valor
        except ValueError:
            print("Ingrese un número entero válido.")


def seleccionar_de_lista(lista, etiqueta):
    if not lista:
        print(f"No hay {etiqueta} registrados.")
        return None
    print()
    for i, item in enumerate(lista, 1):
        print(f"[{i}] {item.describir()}")
    idx = leer_entero(f"\nSeleccione {etiqueta} (número): ", 1)
    if idx > len(lista):
        print("Número fuera de rango.")
        return None
    return lista[idx - 1]


# --- CLIENTES ---

def registrar_cliente():
    print("\n-- Registrar cliente --")
    try:
        nombre   = input("Nombre completo   : ").strip()
        email    = input("Correo electrónico: ").strip()
        telefono = input("Teléfono          : ").strip()
        cliente = Cliente(nombre, email, telefono)
        clientes.append(cliente)
        log.info(f"Cliente registrado: {cliente.describir()}")
        print(f"\nCliente registrado: {cliente.describir()}")
    except (ClienteNombreInvalidoError, ClienteEmailInvalidoError,
            ClienteTelefonoInvalidoError) as e:
        log.error(str(e))
        print(f"Error: {e}")
    pausar()


def listar_clientes():
    print("\n-- Clientes registrados --")
    if not clientes:
        print("No hay clientes registrados.")
    else:
        for i, c in enumerate(clientes, 1):
            print(f"[{i}] {c.describir()} - Reservas: {len(c.reservas)}")
    pausar()


def buscar_cliente():
    print("\n-- Buscar cliente --")
    termino = input("Nombre o email: ").strip().lower()
    encontrados = [c for c in clientes
                   if termino in c.nombre.lower() or termino in c.email.lower()]
    if not encontrados:
        print("No se encontraron clientes.")
    else:
        for c in encontrados:
            print(f"-> {c.describir()}")
    pausar()


def menu_clientes():
    while True:
        print("\n=== CLIENTES ===")
        print("[1] Registrar cliente")
        print("[2] Listar clientes")
        print("[3] Buscar cliente")
        print("[0] Volver")
        op = input("Opción: ").strip()
        if op == "1":
            registrar_cliente()
        elif op == "2":
            listar_clientes()
        elif op == "3":
            buscar_cliente()
        elif op == "0":
            break


# --- SERVICIOS ---

def crear_reserva_sala():
    print("\n-- Nueva sala --")
    try:
        nombre    = input("Nombre de la sala     : ").strip() or "Sala de Reuniones"
        capacidad = leer_entero("Capacidad (personas)  : ", 1)
        premium   = input("¿Es premium? (s/n)    : ").lower() == "s"
        disp      = input("¿Disponible? (s/n)    : ").lower() != "n"
        precio_s  = input("Precio/hora (ENTER=base): ").strip()
        precio    = float(precio_s) if precio_s else None
        sala = ReservaSala(nombre=nombre, capacidad=capacidad,
                           es_premium=premium, precio_hora=precio, disponible=disp)
        servicios.append(sala)
        log.info(f"Sala creada: {sala.describir()}")
        print(f"Sala creada: {sala.describir()}")
    except (ServicioCapacidadExcedidaError, ServicioParametroInvalidoError,
            ServicioPrecioInvalidoError) as e:
        log.error(str(e))
        print(f"Error: {e}")
    pausar()


def crear_alquiler_equipo():
    print("\n-- Nuevo equipo --")
    print("Tipos: laptop | proyector | tablet | servidor | camara")
    try:
        nombre   = input("Nombre del equipo       : ").strip() or "Equipo"
        tipo     = input("Tipo                    : ").strip().lower()
        cantidad = leer_entero("Cantidad disponible     : ", 0)
        alta     = input("¿Alta gama? (s/n)       : ").lower() == "s"
        disp     = input("¿Disponible? (s/n)      : ").lower() != "n"
        precio_s = input("Precio/hora (ENTER=base): ").strip()
        precio   = float(precio_s) if precio_s else None
        equipo = AlquilerEquipo(nombre=nombre, tipo_equipo=tipo,
                                cantidad_disponible=cantidad, alta_gama=alta,
                                precio_hora=precio, disponible=disp)
        servicios.append(equipo)
        log.info(f"Equipo registrado: {equipo.describir()}")
        print(f"Equipo registrado: {equipo.describir()}")
    except ServicioParametroInvalidoError as e:
        log.error(str(e))
        print(f"Error: {e}")
    pausar()


def crear_asesoria():
    print("\n-- Nueva asesoría --")
    print("Niveles: junior | senior | experto")
    print("Modalidades: presencial | virtual")
    try:
        nombre   = input("Título              : ").strip() or "Asesoría"
        area     = input("Área temática       : ").strip() or "Tecnología"
        nivel    = input("Nivel del asesor    : ").strip().lower()
        modal    = input("Modalidad           : ").strip().lower()
        disp     = input("¿Disponible? (s/n)  : ").lower() != "n"
        precio_s = input("Precio/hora (ENTER=base): ").strip()
        precio   = float(precio_s) if precio_s else None
        asesoria = Asesoria(nombre=nombre, area=area, nivel_asesor=nivel,
                            modalidad=modal, precio_hora=precio, disponible=disp)
        servicios.append(asesoria)
        log.info(f"Asesoría creada: {asesoria.describir()}")
        print(f"Asesoría creada: {asesoria.describir()}")
    except ServicioParametroInvalidoError as e:
        log.error(str(e))
        print(f"Error: {e}")
    pausar()


def listar_servicios():
    print("\n-- Servicios registrados --")
    if not servicios:
        print("No hay servicios registrados.")
    else:
        for i, s in enumerate(servicios, 1):
            print(f"[{i}] {s.describir()}")
    pausar()


def calcular_costos_servicio():
    print("\n-- Calcular costos --")
    srv = seleccionar_de_lista(servicios, "servicio")
    if not srv:
        pausar()
        return
    try:
        horas   = leer_entero("Horas a calcular: ", 1)
        base    = srv.calcular_costo(horas)
        con_iva = srv.calcular_costo_con_impuesto(horas)
        con_dto = srv.calcular_costo_con_descuento(horas, 0.10)
        print(f"\nServicio  : {srv.nombre}")
        print(f"Horas     : {horas}")
        print(f"Costo base: ${base:,.2f} COP")
        print(f"Con IVA   : ${con_iva:,.2f} COP")
        print(f"Desc. 10% : ${con_dto:,.2f} COP")
        log.info(f"Cálculo {srv.nombre} | {horas}h | ${base:,.2f}")
    except SoftwareFJError as e:
        print(f"Error: {e}")
    pausar()


def menu_servicios():
    while True:
        print("\n=== SERVICIOS ===")
        print("[1] Nueva sala")
        print("[2] Nuevo equipo")
        print("[3] Nueva asesoría")
        print("[4] Listar servicios")
        print("[5] Calcular costos")
        print("[0] Volver")
        op = input("Opción: ").strip()
        if op == "1":
            crear_reserva_sala()
        elif op == "2":
            crear_alquiler_equipo()
        elif op == "3":
            crear_asesoria()
        elif op == "4":
            listar_servicios()
        elif op == "5":
            calcular_costos_servicio()
        elif op == "0":
            break


# --- RESERVAS ---

def crear_reserva():
    print("\n-- Nueva reserva --")
    try:
        print("\nSeleccione el CLIENTE:")
        cliente = seleccionar_de_lista(clientes, "cliente")
        if not cliente:
            pausar()
            return
        print("\nSeleccione el SERVICIO:")
        servicio = seleccionar_de_lista(servicios, "servicio")
        if not servicio:
            pausar()
            return
        duracion  = leer_entero("Duración en horas: ", 1)
        desc_s    = input("Descuento 0-99% (ENTER=0): ").strip()
        descuento = float(desc_s) / 100 if desc_s else 0.0
        if not (0.0 <= descuento < 1.0):
            print("Descuento fuera de rango, se usará 0%.")
            descuento = 0.0
        iva = input("¿Aplicar IVA 19%? (s/n): ").lower() != "n"
        reserva = Reserva(cliente=cliente, servicio=servicio,
                          duracion_horas=duracion, descuento=descuento,
                          aplicar_impuesto=iva)
        reservas.append(reserva)
        log.info(f"Reserva creada: {reserva.describir()}")
        print(f"\nReserva creada (PENDIENTE): {reserva.describir()}")
    except (ReservaDuracionInvalidaError, ServicioNoDisponibleError) as e:
        log.error(str(e))
        print(f"Error: {e}")
    pausar()


def confirmar_reserva():
    print("\n-- Confirmar reserva --")
    pendientes = [r for r in reservas if r.estado == "pendiente"]
    if not pendientes:
        print("No hay reservas pendientes.")
        pausar()
        return
    reserva = seleccionar_de_lista(pendientes, "reserva pendiente")
    if not reserva:
        pausar()
        return
    try:
        reserva.confirmar()
        log.info(f"Reserva confirmada: {reserva.id_reserva}")
        print(f"Confirmada: {reserva.describir()}")
    except ReservaEstadoInvalidoError as e:
        print(f"Error: {e}")
    pausar()


def procesar_reserva():
    print("\n-- Procesar reserva --")
    confirmadas = [r for r in reservas if r.estado == "confirmada"]
    if not confirmadas:
        print("No hay reservas confirmadas.")
        pausar()
        return
    reserva = seleccionar_de_lista(confirmadas, "reserva confirmada")
    if not reserva:
        pausar()
        return
    try:
        costo = reserva.procesar()
        log.info(f"Reserva procesada: {reserva.id_reserva} | ${costo:,.2f}")
        print(f"Procesada. Costo total: ${costo:,.2f} COP")
        print(reserva.describir())
    except (ReservaEstadoInvalidoError, ReservaCostoInconsistenteError) as e:
        print(f"Error: {e}")
    pausar()


def cancelar_reserva():
    print("\n-- Cancelar reserva --")
    cancelables = [r for r in reservas if r.estado in ("pendiente", "confirmada")]
    if not cancelables:
        print("No hay reservas que se puedan cancelar.")
        pausar()
        return
    reserva = seleccionar_de_lista(cancelables, "reserva")
    if not reserva:
        pausar()
        return
    confirmar = input(f"¿Cancelar la reserva {reserva.id_reserva}? (s/n): ").lower()
    if confirmar != "s":
        print("Cancelación abortada.")
        pausar()
        return
    try:
        reserva.cancelar()
        log.info(f"Reserva cancelada: {reserva.id_reserva}")
        print(f"Cancelada: {reserva.describir()}")
    except ReservaEstadoInvalidoError as e:
        print(f"Error: {e}")
    pausar()


def listar_reservas():
    print("\n-- Todas las reservas --")
    if not reservas:
        print("No hay reservas registradas.")
    else:
        iconos = {"pendiente": "[P]", "confirmada": "[C]",
                  "procesada": "[OK]", "cancelada": "[X]"}
        for i, r in enumerate(reservas, 1):
            icono = iconos.get(r.estado, "[ ]")
            print(f"[{i}] {icono} {r.describir()}")
    pausar()


def menu_reservas():
    while True:
        print("\n=== RESERVAS ===")
        print("[1] Crear reserva")
        print("[2] Confirmar reserva")
        print("[3] Procesar reserva")
        print("[4] Cancelar reserva")
        print("[5] Listar reservas")
        print("[0] Volver")
        op = input("Opción: ").strip()
        if op == "1":
            crear_reserva()
        elif op == "2":
            confirmar_reserva()
        elif op == "3":
            procesar_reserva()
        elif op == "4":
            cancelar_reserva()
        elif op == "5":
            listar_reservas()
        elif op == "0":
            break


# --- DEMO ---

def op1_cliente_valido():
    log.separador("OP-01 | Cliente válido")
    try:
        c = Cliente("Ana Lucía Martínez", "ana.martinez@softwarefj.com", "+57 310 4567890")
        log.info(f"Cliente creado: {c.describir()}")
        clientes.append(c)
        return c
    except SoftwareFJError as e:
        log.error(f"Error en OP-01: {e}", e)


def op2_clientes_invalidos():
    log.separador("OP-02 | Clientes inválidos")
    casos = [
        ("A", "ok@mail.com", "3101234567"),
        ("Pedro Pérez", "correo-sin-arroba", "3101234567"),
        ("Pedro Pérez", "pedro@mail.com", "123"),
        ("12345 nombre", "x@x.com", "3001234567"),
    ]
    for nombre, email, telefono in casos:
        try:
            Cliente(nombre, email, telefono)
        except (ClienteNombreInvalidoError, ClienteEmailInvalidoError,
                ClienteTelefonoInvalidoError) as e:
            log.error(f"Capturado: {e}")
        finally:
            log.info("  Intento procesado.")


def op3_servicios_validos():
    log.separador("OP-03 | Servicios válidos")
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
        log.info("Todos los servicios creados correctamente.")
    finally:
        log.info("OP-03 finalizada.")
    return svcs


def op4_servicios_invalidos():
    log.separador("OP-04 | Servicios inválidos")
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
    log.separador("OP-05 | Cálculo de costos")
    if not svcs:
        log.advertencia("Sin servicios para OP-05.")
        return
    for srv in svcs:
        h = 3
        b = srv.calcular_costo(h)
        v = srv.calcular_costo_con_impuesto(h)
        d = srv.calcular_costo_con_descuento(h, 0.10)
        log.info(f"  {srv.nombre} | Base:${b:,.2f} | IVA:${v:,.2f} | -10%:${d:,.2f}")
    log.info("OP-05 finalizada.")


def op6_reserva_exitosa(cliente, svcs):
    log.separador("OP-06 | Reserva completa")
    if not cliente or not svcs:
        log.advertencia("Datos insuficientes.")
        return None
    reserva = None
    try:
        sala = svcs[0]
        sala.validar_parametros(personas=10)
        reserva = Reserva(cliente, sala, duracion_horas=4, descuento=0.05,
                          aplicar_impuesto=True)
        log.info(f"Creada: {reserva.describir()}")
        reserva.confirmar()
        log.info(f"Confirmada: {reserva.estado}")
        costo = reserva.procesar()
        log.info(f"Procesada - Costo: ${costo:,.2f}")
        reservas.append(reserva)
    except SoftwareFJError as e:
        log.error(f"Error en OP-06: {e}", e)
    else:
        log.info("Reserva completada sin errores.")
    finally:
        log.info("OP-06 finalizada.")
    return reserva


def op7_reserva_duracion_invalida(cliente, svcs):
    log.separador("OP-07 | Duración inválida")
    if not cliente or not svcs:
        return
    try:
        Reserva(cliente, svcs[0], duracion_horas=-5)
    except ReservaDuracionInvalidaError as e:
        log.error(f"Capturado: {e}")
    finally:
        log.info("OP-07 finalizada.")


def op8_servicio_no_disponible(cliente):
    log.separador("OP-08 | Servicio no disponible")
    if not cliente:
        return
    try:
        sala = ReservaSala("Sala en Mantenimiento", capacidad=5, disponible=False)
        Reserva(cliente, sala, duracion_horas=2)
    except ServicioNoDisponibleError as e:
        log.error(f"Capturado: {e}")
    finally:
        log.info("OP-08 finalizada.")


def op9_estado_invalido(reserva_proc):
    log.separador("OP-09 | Cancelar reserva ya procesada")
    if not reserva_proc:
        return
    try:
        reserva_proc.cancelar()
    except ReservaEstadoInvalidoError as e:
        log.error(f"Capturado: {e}")
    finally:
        log.info("OP-09 finalizada.")


def op10_encadenamiento(cliente, svcs):
    log.separador("OP-10 | Encadenamiento de excepciones")
    if not cliente or not svcs:
        return
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
        log.error(f"Error: {e}", e)
    finally:
        log.info("OP-10 finalizada.")


def op11_stock_insuficiente(cliente):
    log.separador("OP-11 | Stock insuficiente")
    if not cliente:
        return
    try:
        equipo = AlquilerEquipo("Tablet Samsung", tipo_equipo="tablet",
                                cantidad_disponible=2)
        log.info(f"Equipo: {equipo.describir()}")
        equipo.validar_parametros(cantidad=10)
    except ServicioNoDisponibleError as e:
        log.error(f"Capturado: {e}")
    finally:
        log.info("OP-11 finalizada.")


def op12_asesoria_virtual(cliente):
    log.separador("OP-12 | Asesoría virtual con descuento")
    if not cliente:
        return
    try:
        asesoria = Asesoria("Consultoría Cloud", area="Infraestructura",
                            nivel_asesor="senior", modalidad="virtual")
        log.info(f"Servicio: {asesoria.describir()}")
        r = Reserva(cliente, asesoria, duracion_horas=3,
                    descuento=0.08, aplicar_impuesto=True)
        r.confirmar()
        costo = r.procesar()
        log.info(f"Procesada - Costo: ${costo:,.2f}")
        reservas.append(r)
    except SoftwareFJError as e:
        log.error(f"Error en OP-12: {e}", e)
    else:
        log.info("OP-12 completada sin errores.")
    finally:
        log.info("OP-12 finalizada.")


def ejecutar_demo():
    print("\n=== DEMO - 12 operaciones automáticas ===")
    print("Los datos quedarán disponibles en los menús.")
    if input("¿Continuar? (s/n): ").lower() != "s":
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
    print("\nDemo completada. Ver logs/eventos.log")
    pausar()


# --- RESUMEN ---

def mostrar_resumen():
    print("\n=== RESUMEN ===")
    pendientes  = sum(1 for r in reservas if r.estado == "pendiente")
    confirmadas = sum(1 for r in reservas if r.estado == "confirmada")
    procesadas  = sum(1 for r in reservas if r.estado == "procesada")
    canceladas  = sum(1 for r in reservas if r.estado == "cancelada")
    ingresos    = sum(r.costo_total for r in reservas if r.estado == "procesada")
    print(f"Clientes   : {len(clientes)}")
    print(f"Servicios  : {len(servicios)}")
    print(f"Reservas   : {len(reservas)}")
    print(f"  Pendientes  : {pendientes}")
    print(f"  Confirmadas : {confirmadas}")
    print(f"  Procesadas  : {procesadas}")
    print(f"  Canceladas  : {canceladas}")
    print(f"Ingresos    : ${ingresos:,.2f} COP")
    log.info(f"Resumen - C:{len(clientes)} S:{len(servicios)} R:{len(reservas)} I:${ingresos:,.2f}")
    pausar()


# --- MENÚ PRINCIPAL ---

def main():
    while True:
        print(f"\n=== SISTEMA SOFTWARE FJ ===")
        print(f"Clientes: {len(clientes)} | Servicios: {len(servicios)} | Reservas: {len(reservas)}")
        print("[1] Clientes")
        print("[2] Servicios")
        print("[3] Reservas")
        print("[4] Resumen")
        print("[5] Demo")
        print("[0] Salir")
        op = input("Opción: ").strip()
        if op == "1":
            menu_clientes()
        elif op == "2":
            menu_servicios()
        elif op == "3":
            menu_reservas()
        elif op == "4":
            mostrar_resumen()
        elif op == "5":
            ejecutar_demo()
        elif op == "0":
            log.info("Sistema cerrado.")
            print("Hasta luego.")
            sys.exit(0)


if __name__ == "__main__":
    main()
