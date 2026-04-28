#  Sistema de Relojes Analógicos

Aplicación de escritorio en Python que muestra **tres relojes analógicos en tiempo real** (Hora Local, Nueva York y Tokio) con un sistema de alarmas configurable. 

---

##  Vista General

La ventana principal muestra:

- **3 relojes analógicos** sincronizados, actualizados cada 100 ms.
- **Panel de control** para agregar y gestionar alarmas.
- **Historial de alarmas** disparadas con marca de tiempo.

---

##  Estructura del Proyecto

```
Taller-Reloj/
│
├── main.py            # Punto de entrada de la aplicación
├── clock_app.py       # Orquestador principal (ventana Tkinter)
├── clock_widget.py    # Componente visual del reloj analógico
├── clock_hand.py      # Lógica y geometría de las manecillas
├── clock_time.py      # Lógica pura de tiempo y cálculo de ángulos
├── alarm.py           # Modelo de una alarma individual
└── alarm_manager.py   # Gestor de alarmas (CRUD + historial)
```


##  Características

- **3 zonas horarias simultáneas:** Hora Local, Nueva York (UTC-4) y Tokio (UTC+9).
- **Relojes analógicos animados** con manecillas de hora, minuto y segundo.
- **Alarmas configurables** con:
  - Hora en formato 24h.
  - Mensaje personalizado.
  - Repetición automática cada N minutos (o diaria).
- **Notificación de alarma** con:
  - Sonido (beeps del sistema vía `winsound`).
  - Parpadeo visual de la ventana.
  - Cuadro de diálogo informativo.
- **Historial de alarmas** disparadas con marca de tiempo exacta.

---

### Ejecutar

```bash
python main.py
```

---

##  Cómo usar las alarmas

1. Haz clic en el botón **"+ Añadir Alarma"**.
2. Ingresa la **hora** en formato `HH:MM` (24h, basada en la Hora Local).
3. Escribe un **mensaje** descriptivo para la alarma.
4. Define cada cuántos **minutos** se repetirá (escribe `0` para que suene solo una vez por día a esa hora).
5. Cuando llegue la hora, la ventana **parpadeará**, sonará un **beep** y aparecerá una **notificación**.
6. El evento quedará registrado en el **Historial de Alarmas**.

<<<<<<< HEAD
---

##  Diseño Visual

| Elemento | Color |
|---|---|
| Fondo de la aplicación | `#2c3e50` (azul oscuro) |
| Esfera del reloj | `#1abc9c` (verde esmeralda) |
| Manecilla de horas | `#ecf0f1` (blanco perla) |
| Manecilla de minutos | `#bdc3c7` (gris claro) |
| Segundero | `#e74c3c` (rojo vivo) |
| Alerta de alarma | `#e74c3c` (parpadeo rojo) |

---
=======

>>>>>>> 80aaa7961b96043be8bf9c660de8b021b182efa3
