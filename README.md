# Sistema Integral de Gestión de Clientes

Proyecto desarrollado para la materia de Programación en la UNAD.

Este sistema permite administrar clientes, servicios y reservas desde consola usando Python y programación orientada a objetos. Toda la información se maneja en memoria, por lo que no es necesario usar base de datos.

---

## Características principales

- Registro y búsqueda de clientes
- Gestión de distintos tipos de servicios
- Creación, confirmación y cancelación de reservas
- Validaciones de datos
- Manejo de excepciones personalizadas
- Registro de eventos en archivo `.log`
- Menú interactivo en consola

---

## Tecnologías utilizadas

- Python 3
- Programación Orientada a Objetos (POO)
- Manejo de excepciones
- Archivos y logs

---

## Estructura del proyecto

```bash
Sistema_Integral_De_Gestion_De_Clientes/
│
├── main.py
├── logs/
├── models/
├── services/
├── exceptions/
└── utils/
```

---

## Cómo ejecutar el proyecto

Desde la terminal:

```bash
python main.py
```

No necesita instalar librerías externas.

---

## Funcionalidades

### Clientes

- Registrar clientes
- Validar nombre, correo y teléfono
- Consultar clientes registrados

### Servicios

El sistema maneja varios tipos de servicios:

- Reserva de salas
- Alquiler de equipos
- Asesorías

Cada servicio calcula costos de manera diferente.

### Reservas

Las reservas tienen distintos estados:

```text
Pendiente → Confirmada → Procesada
```

También pueden cancelarse dependiendo del estado.

---

## Conceptos de POO aplicados

- Herencia
- Polimorfismo
- Encapsulación
- Abstracción

Además, se implementaron clases abstractas y validaciones usando propiedades.

---

## Manejo de errores

El proyecto incluye excepciones personalizadas para controlar errores como:

- Datos inválidos
- Servicios no disponibles
- Reservas incorrectas
- Problemas de validación

Todos los eventos importantes se guardan en:

```bash
logs/eventos.log
```

---

## Autor

Desarrollado por Software FJ como proyecto académico para la UNAD.
