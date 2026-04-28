import tkinter as tk
from tkinter import messagebox
import winsound
import time
import threading
from datetime import datetime, timedelta

from alarm_manager import AlarmManager
from clock_widget import ClockWidget, StopwatchWidget
from styles import *

class CustomAlarmDialog(tk.Toplevel):
    """Diálogo personalizado para crear una alarma."""
    def __init__(self, parent, title="Nueva Alarma"):
        super().__init__(parent)
        self.title(title)
        self.geometry("300x280")
        self.resizable(False, False)
        self.configure(bg=get_style("frame_bg"))
        self.result = None
        self.transient(parent)
        self.grab_set()

        tk.Label(self, text="Configurar Alarma", bg=get_style("frame_bg"), fg=get_style("accent"),
                 font=FONT_BOLD).pack(pady=10)

        # Hora y minuto
        time_frame = tk.Frame(self, bg=get_style("frame_bg"))
        time_frame.pack(pady=5)
        tk.Label(time_frame, text="Hora:", bg=get_style("frame_bg"), fg=get_style("text")).pack(side=tk.LEFT)
        self.hour_spin = tk.Spinbox(time_frame, from_=0, to=23, width=3, format="%02.0f")
        self.hour_spin.pack(side=tk.LEFT, padx=5)
        tk.Label(time_frame, text="Min:", bg=get_style("frame_bg"), fg=get_style("text")).pack(side=tk.LEFT)
        self.min_spin = tk.Spinbox(time_frame, from_=0, to=59, width=3, format="%02.0f")
        self.min_spin.pack(side=tk.LEFT, padx=5)

        # Mensaje
        tk.Label(self, text="Mensaje:", bg=get_style("frame_bg"), fg=get_style("text")).pack(pady=(10, 0))
        self.msg_entry = tk.Entry(self, width=30)
        self.msg_entry.insert(0, "¡Alarma!")
        self.msg_entry.pack(pady=5)

        # Repetición
        tk.Label(self, text="Repetir cada N min (0 = diario):", bg=get_style("frame_bg"), fg=get_style("text")).pack()
        self.rep_spin = tk.Spinbox(self, from_=0, to=1440, width=5)
        self.rep_spin.pack(pady=5)

        # Botones
        btn_frame = tk.Frame(self, bg=get_style("frame_bg"))
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Cancelar", command=self.destroy,
                  bg=get_style("alert"), fg="#ffffff", width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Guardar", command=self.save,
                  bg=get_style("button_bg"), fg=get_style("button_fg"), width=10).pack(side=tk.LEFT, padx=5)

    def save(self):
        try:
            h = int(self.hour_spin.get())
            m = int(self.min_spin.get())
            msg = self.msg_entry.get() or "¡Alarma!"
            rep = int(self.rep_spin.get())
            self.result = (h, m, msg, rep)
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Valores inválidos")

class ClockApp(tk.Tk):
    """Ventana principal con temas, animaciones suaves y cronómetro."""
    def __init__(self):
        super().__init__()
        self.title("Sistema de Relojes Analógicos Pro")
        self.geometry("950x550")
        self.configure(bg=get_style("bg"))
        self.alarm_manager = AlarmManager()
        
        # Variables para el cronómetro
        self.sw_running = False
        self.sw_start_time = None
        self.sw_elapsed = timedelta(0)

        self.setup_ui()
        self.update_clocks()

    def setup_ui(self):
        # Header con toggle de tema
        header = tk.Frame(self, bg=get_style("bg"))
        header.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(header, text="🕒 Relojes del Mundo", bg=get_style("bg"), fg=get_style("text"), 
                 font=(FONT_FAMILY, 16, "bold")).pack(side=tk.LEFT)
        
        self.theme_btn = tk.Button(header, text="🌓 Cambiar Tema", command=self.change_theme,
                                   bg=get_style("button_bg"), fg=get_style("button_fg"), font=FONT_SMALL)
        self.theme_btn.pack(side=tk.RIGHT)

        # Frame de Relojes
        self.clocks_frame = tk.Frame(self, bg=get_style("frame_bg"), relief=tk.RIDGE, bd=1)
        self.clocks_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)
        
        self.clock_local = ClockWidget(self.clocks_frame, "Hora Local", offset_hours=None, size=220)
        self.clock_local.pack(side=tk.LEFT, expand=True, padx=5)
        self.clock_ny = ClockWidget(self.clocks_frame, "Nueva York (UTC-4)", offset_hours=-4, size=220)
        self.clock_ny.pack(side=tk.LEFT, expand=True, padx=5)
        self.clock_tokyo = ClockWidget(self.clocks_frame, "Tokio (UTC+9)", offset_hours=9, size=220)
        self.clock_tokyo.pack(side=tk.LEFT, expand=True, padx=5)

        # Bottom section: Alarmas y Cronómetro
        self.bottom_frame = tk.Frame(self, bg=get_style("bg"))
        self.bottom_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Alarmas (Izquierda)
        self.alarm_frame = tk.Frame(self.bottom_frame, bg=get_style("frame_bg"), padx=10, pady=10, relief=tk.RIDGE, bd=1)
        self.alarm_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.add_alarm_btn = tk.Button(self.alarm_frame, text="⏰ Nueva Alarma",
                                        command=self.add_alarm_dialog, bg=get_style("button_bg"), fg=get_style("button_fg"),
                                        font=FONT_NORMAL, cursor="hand2", width=20)
        self.add_alarm_btn.pack(pady=5)
        
        self.alarms_label = tk.Label(self.alarm_frame, text="Alarmas activas: 0",
                                      bg=get_style("frame_bg"), fg=get_style("text"), font=FONT_BOLD)
        self.alarms_label.pack(pady=5)

        # Cronómetro (Derecha)
        self.sw_frame = tk.Frame(self.bottom_frame, bg=get_style("frame_bg"), padx=10, pady=10, relief=tk.RIDGE, bd=1)
        self.sw_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(self.sw_frame, text="⏱️ Cronómetro Analógico", bg=get_style("frame_bg"), fg=get_style("text"), font=FONT_BOLD).pack()
        
        self.sw_analog = StopwatchWidget(self.sw_frame, "", size=180)
        self.sw_analog.pack(pady=5)
        
        self.sw_label = tk.Label(self.sw_frame, text="00:00:00.0", bg=get_style("frame_bg"), 
                                  fg=get_style("accent"), font=("Consolas", 14, "bold"))
        self.sw_label.pack(pady=2)
        
        sw_btns = tk.Frame(self.sw_frame, bg=get_style("frame_bg"))
        sw_btns.pack()
        self.sw_start_btn = tk.Button(sw_btns, text="Iniciar", command=self.toggle_stopwatch, 
                                       bg="#27ae60", fg="white", width=8)
        self.sw_start_btn.pack(side=tk.LEFT, padx=5)
        tk.Button(sw_btns, text="Reiniciar", command=self.reset_stopwatch, 
                  bg=get_style("secondary"), fg="white", width=8).pack(side=tk.LEFT, padx=5)

    def change_theme(self):
        toggle_theme()
        # Actualizar ventana principal
        self.configure(bg=get_style("bg"))
        for widget in [self.clocks_frame, self.bottom_frame, self.alarm_frame, self.sw_frame]:
            widget.configure(bg=get_style("frame_bg") if widget != self.bottom_frame else get_style("bg"))
        
        # Actualizar botones y etiquetas
        self.theme_btn.configure(bg=get_style("button_bg"), fg=get_style("button_fg"))
        self.add_alarm_btn.configure(bg=get_style("button_bg"), fg=get_style("button_fg"))
        self.alarms_label.configure(bg=get_style("frame_bg"), fg=get_style("text"))
        self.sw_label.configure(bg=get_style("frame_bg"), fg=get_style("text"))
        self.sw_frame.winfo_children()[0].configure(bg=get_style("frame_bg"), fg=get_style("text")) # SW Title
        
        # Actualizar Relojes
        self.clock_local.update_styles()
        self.clock_ny.update_styles()
        self.clock_tokyo.update_styles()
        self.sw_analog.update_styles()

    def toggle_stopwatch(self):
        if not self.sw_running:
            self.sw_running = True
            self.sw_start_time = datetime.now() - self.sw_elapsed
            self.sw_start_btn.config(text="Pausar", bg="#e67e22")
        else:
            self.sw_running = False
            self.sw_elapsed = datetime.now() - self.sw_start_time
            self.sw_start_btn.config(text="Iniciar", bg="#27ae60")

    def reset_stopwatch(self):
        self.sw_running = False
        self.sw_elapsed = timedelta(0)
        self.sw_label.config(text="00:00:00.0")
        self.sw_start_btn.config(text="Iniciar", bg="#27ae60")

    def update_stopwatch(self):
        if self.sw_running:
            self.sw_elapsed = datetime.now() - self.sw_start_time
        
        total_seconds = self.sw_elapsed.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        micros = int((total_seconds % 1) * 1_000_000)
        decimos = micros // 100_000
        
        # Actualizar tanto el texto como el reloj analógico
        self.sw_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}.{decimos}")
        self.sw_analog.draw_stopwatch(hours, minutes, seconds, micros)

    def update_clocks(self):
        # Actualización suave cada 50ms
        l_h, l_m, l_s = self.clock_local.update_clock()
        self.clock_ny.update_clock()
        self.clock_tokyo.update_clock()
        
        # Solo check alarmas cada segundo (cuando l_s cambia)
        if not hasattr(self, '_last_s') or self._last_s != l_s:
            triggered = self.alarm_manager.check_alarms(l_h, l_m)
            for alarm in triggered:
                self.trigger_alarm(alarm)
            self._last_s = l_s
            self.update_alarms_label()
        
        self.update_stopwatch()
        self.after(50, self.update_clocks)

    def add_alarm_dialog(self):
        dlg = CustomAlarmDialog(self)
        self.wait_window(dlg)
        if dlg.result:
            h, m, msg, rep = dlg.result
            self.alarm_manager.add_alarm(h, m, msg, rep)
            self.update_alarms_label()
            messagebox.showinfo("Alarma", "Alarma programada correctamente")

    def update_alarms_label(self):
        active = len([a for a in self.alarm_manager.alarms if a.enabled])
        self.alarms_label.config(text=f"Alarmas activas: {active}")

    def trigger_alarm(self, alarm):
        def play():
            for _ in range(3):
                winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
                time.sleep(0.3)
        threading.Thread(target=play, daemon=True).start()
        messagebox.showinfo("¡ALERTA!", f"⏰ {alarm.hour:02d}:{alarm.minute:02d}\n{alarm.message}")

if __name__ == "__main__":
    app = ClockApp()
    app.mainloop()
