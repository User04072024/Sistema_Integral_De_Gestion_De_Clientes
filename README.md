# Sistema Integral de Gestión de Clientes, Servicios y Reservas
**Empresa:** Software FJ  
**Curso:** Programación (213023) — UNAD  
**Escuela:** ECBTI — Ingeniería de Sistemas

---

## Descripción

Sistema orientado a objetos con **menú interactivo** que gestiona clientes, servicios y reservas sin uso de base de datos. Implementa los principios de **abstracción, herencia, polimorfismo, encapsulación** y **manejo avanzado de excepciones**. Todos los datos se manejan en memoria mediante listas de objetos; el archivo `logs/eventos.log` registra todos los eventos y errores.

---

## Estructura del Proyecto

```
Sistema_Integral_De_Gestion_De_Clientes/
│
├── main.py                        # Punto de entrada — Menú interactivo + 12 operaciones demo
├── logs/
│   └── eventos.log                # Registro de eventos y errores (auto-generado)
├── models/
│   ├── entidad.py                 # Clase abstracta base (ABC)
│   ├── cliente.py                 # Clase Cliente con encapsulación y validaciones
│   ├── servicio.py                # Clase abstracta Servicio
│   └── reserva.py                 # Clase Reserva — ciclo de vida completo
├── services/
│   ├── reserva_sala.py            # Servicio: Reserva de Sala (estándar/premium)
│   ├── alquiler_equipo.py         # Servicio: Alquiler de Equipos tecnológicos
│   └── asesoria.py                # Servicio: Asesoría Especializada (junior/senior/experto)
├── exceptions/
│   └── custom_exceptions.py       # Jerarquía de excepciones personalizadas
└── utils/
    └── logger.py                  # Logger Singleton — escribe en logs/eventos.log
```

---

## Cómo Ejecutar

```bash
python main.py
```

> Requiere Python 3.9+. No necesita dependencias externas ni base de datos.

---

## Menú Interactivo

Al ejecutar el programa aparece el menú principal con las siguientes opciones:

```
══════════════════════════════════════════════════════════
  SISTEMA INTEGRAL DE GESTIÓN — Software FJ
══════════════════════════════════════════════════════════
  Clientes: 0  |  Servicios: 0  |  Reservas: 0

  [1] Gestión de Clientes
  [2] Gestión de Servicios
  [3] Gestión de Reservas
  [4] Resumen del sistema
  [5] Ejecutar Demo (12 operaciones automáticas)
  [0] Salir
```

### [1] Gestión de Clientes
- Registrar nuevo cliente (nombre, email, teléfono con validación)
- Listar todos los clientes con su historial de reservas
- Buscar cliente por nombre o email

### [2] Gestión de Servicios
- Crear Reserva de Sala (capacidad, tipo estándar/premium, precio/hora)
- Crear Alquiler de Equipo (tipo, cantidad en stock, gama)
- Crear Asesoría Especializada (área, nivel, modalidad presencial/virtual)
- Listar todos los servicios
- Calcular costos de un servicio (base, con IVA, con descuento)

### [3] Gestión de Reservas
- Crear nueva reserva → estado **PENDIENTE** (selecciona cliente y servicio)
- Confirmar reserva → estado **CONFIRMADA**
- Procesar reserva → estado **PROCESADA** (calcula y muestra el costo final)
- Cancelar reserva (solo PENDIENTE o CONFIRMADA)
- Listar todas las reservas con indicador de estado por color

### [4] Resumen del sistema
Muestra estadísticas en tiempo real: total de clientes, servicios, reservas por estado e ingresos acumulados.

### [5] Demo automática
Ejecuta las 12 operaciones predefinidas descritas más abajo. Los datos cargados por la demo quedan disponibles en los menús interactivos.

---

## Ciclo de Vida de una Reserva

```
CREAR → [PENDIENTE] → confirmar() → [CONFIRMADA] → procesar() → [PROCESADA]
                   ↘ cancelar()  ↗ cancelar()
                              [CANCELADA]
```

---

## Principios OOP Implementados

| Principio        | Dónde se aplica |
|------------------|-----------------|
| **Abstracción**  | `Entidad` (ABC), `Servicio` (ABC) con métodos abstractos |
| **Herencia**     | `Cliente → Entidad`, `ReservaSala / AlquilerEquipo / Asesoria → Servicio → Entidad` |
| **Polimorfismo** | `calcular_costo()`, `calcular_costo_con_impuesto()`, `calcular_costo_con_descuento()`, `describir()` — implementación distinta en cada clase |
| **Encapsulación**| Atributos privados `__` con propiedades y setters validados en `Cliente`, `Servicio`, `Reserva` |

---

## Manejo de Excepciones

| Técnica                        | Dónde se usa |
|--------------------------------|--------------|
| `try/except`                   | Todos los módulos del menú interactivo y demo OP-02, OP-04, OP-07, OP-08, OP-11 |
| `try/except/else`              | OP-03, OP-06, OP-12 |
| `try/except/finally`           | OP-01, OP-02, OP-05, OP-07, OP-08, OP-09 |
| Encadenamiento (`raise … from`)| OP-10 |
| Registro en archivo logs       | Todas las operaciones |

### Jerarquía de Excepciones Personalizadas

```
SoftwareFJError
├── ClienteError
│   ├── ClienteNombreInvalidoError    (CLI-001)
│   ├── ClienteEmailInvalidoError     (CLI-002)
│   ├── ClienteTelefonoInvalidoError  (CLI-003)
│   ├── ClienteYaExisteError          (CLI-004)
│   └── ClienteNoEncontradoError      (CLI-005)
├── ServicioError
│   ├── ServicioNoDisponibleError     (SRV-001)
│   ├── ServicioPrecioInvalidoError   (SRV-002)
│   ├── ServicioCapacidadExcedidaError(SRV-003)
│   └── ServicioParametroInvalidoError(SRV-004)
├── ReservaError
│   ├── ReservaDuracionInvalidaError  (RES-001)
│   ├── ReservaEstadoInvalidoError    (RES-002)
│   ├── ReservaNoEncontradaError      (RES-003)
│   └── ReservaCostoInconsistenteError(RES-004)
└── LoggerError                       (LOG-001)
```

---

## Operaciones de Demo (12 en total)

| # | Descripción | Resultado esperado |
|---|-------------|-------------------|
| 01 | Registro de cliente válido | ✅ Éxito |
| 02 | Clientes con datos inválidos (4 casos) | ❌ Excepciones capturadas |
| 03 | Creación de 4 servicios válidos | ✅ Éxito + `else` ejecutado |
| 04 | Servicios con parámetros inválidos (4 casos) | ❌ Excepciones capturadas |
| 05 | Cálculo polimórfico de costos (base/IVA/descuento) | ✅ Valores correctos |
| 06 | Reserva completa: pendiente → confirmada → procesada | ✅ Éxito + `else` |
| 07 | Reserva con duración inválida (-5 horas) | ❌ Capturada |
| 08 | Reserva sobre servicio no disponible | ❌ Capturada |
| 09 | Cancelar reserva ya procesada | ❌ Capturada |
| 10 | Encadenamiento de excepciones (`raise X from Y`) | ❌ Capturada con causa |
| 11 | Alquiler con stock insuficiente | ❌ Capturada |
| 12 | Reserva de asesoría virtual senior con descuento | ✅ Éxito |

---

## Servicios Disponibles

### ReservaSala
- Precio base: $80.000 COP/hora · Premium: $104.000 COP/hora (+30%)
- Capacidad máxima: 30 personas
- Valida número de asistentes vs. capacidad

### AlquilerEquipo
- Tipos: `laptop`, `proyector`, `tablet`, `servidor`, `camara`
- Precio base: $45.000 COP/hora · Alta gama: $67.500 COP/hora (+50%)
- Controla stock disponible

### Asesoria
- Niveles: `junior` (×1.0) · `senior` (×1.6) · `experto` (×2.2)
- Modalidades: `presencial` · `virtual` (descuento 10%)
- Precio base junior: $120.000 COP/hora
- Asesor experto: mínimo 2 horas y descuento máximo del 10%

---

## Validaciones Implementadas

| Campo | Regla |
|-------|-------|
| Nombre cliente | Solo letras y espacios, 2–60 caracteres |
| Email cliente | Formato `usuario@dominio.ext` |
| Teléfono cliente | 7–15 dígitos (acepta `+`, `-`, espacios) |
| Precio servicio | Número positivo > 0 |
| Capacidad sala | 1–30 personas |
| Tipo equipo | Solo tipos definidos en lista |
| Nivel asesor | `junior`, `senior` o `experto` |
| Modalidad asesoría | `presencial` o `virtual` |
| Duración reserva | Entero positivo (horas) |
| Descuento reserva | 0.0–0.99 (0%–99%) |
