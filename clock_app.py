import tkinter as tk
from tkinter import messagebox, simpledialog
import winsound
import time
import threading
from datetime import datetime

from alarm_manager import AlarmManager
from clock_widget import ClockWidget

# Colors for professional theme
BG_COLOR = "#f5f5f5"  # Light gray background
FRAME_BG = "#ffffff"  # White frames
ACCENT_COLOR = "#2c3e50"  # Dark blue accent
BUTTON_BG = "#2c3e50"
BUTTON_FG = "#ffffff"
TEXT_COLOR = "#2c3e50"
FONT_FAMILY = "Helvetica"

class CustomAlarmDialog(tk.Toplevel):
    """Diálogo personalizado para crear una alarma de forma sencilla y profesional."""
    def __init__(self, parent, title="Nueva Alarma"):
        super().__init__(parent)
        self.title(title)
        self.geometry("300x260")
        self.resizable(False, False)
        self.configure(bg=FRAME_BG)
        self.result = None
        self.transient(parent)
        self.grab_set()

        tk.Label(self, text="Configurar Alarma", bg=FRAME_BG, fg=ACCENT_COLOR,
                 font=(FONT_FAMILY, 12, "bold")).pack(pady=10)

        # Hora y minuto
        time_frame = tk.Frame(self, bg=FRAME_BG)
        time_frame.pack(pady=5)
        tk.Label(time_frame, text="Hora:", bg=FRAME_BG, fg=TEXT_COLOR).pack(side=tk.LEFT)
        self.hour_spin = tk.Spinbox(time_frame, from_=0, to=23, width=3, format="%02.0f")
        self.hour_spin.pack(side=tk.LEFT, padx=5)
        tk.Label(time_frame, text="Min:", bg=FRAME_BG, fg=TEXT_COLOR).pack(side=tk.LEFT)
        self.min_spin = tk.Spinbox(time_frame, from_=0, to=59, width=3, format="%02.0f")
        self.min_spin.pack(side=tk.LEFT, padx=5)

        # Mensaje
        tk.Label(self, text="Mensaje:", bg=FRAME_BG, fg=TEXT_COLOR).pack(pady=(10, 0))
        self.msg_entry = tk.Entry(self, width=30)
        self.msg_entry.insert(0, "¡Alarma!")
        self.msg_entry.pack(pady=5)

        # Repetición
        tk.Label(self, text="Repetir cada N min (0 = diario):", bg=FRAME_BG, fg=TEXT_COLOR).pack()
        self.rep_spin = tk.Spinbox(self, from_=0, to=1440, width=5)
        self.rep_spin.pack(pady=5)

        # Botones
        btn_frame = tk.Frame(self, bg=FRAME_BG)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Cancelar", command=self.destroy,
                  bg="#e74c3c", fg="#ffffff", width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Guardar", command=self.save,
                  bg=BUTTON_BG, fg=BUTTON_FG, width=10).pack(side=tk.LEFT, padx=5)

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
    """Ventana principal del reloj analógico con un estilo profesional."""
    def __init__(self):
        super().__init__()
        self.title("Sistema de Relojes Analógicos")
        self.geometry("900x460")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)
        self.alarm_manager = AlarmManager()

        # Top frame con los relojes
        clocks_frame = tk.Frame(self, bg=FRAME_BG)
        clocks_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        self.clock_local = ClockWidget(clocks_frame, "Hora Local", offset_hours=None, size=250)
        self.clock_local.pack(side=tk.LEFT, expand=True, padx=5)
        self.clock_ny = ClockWidget(clocks_frame, "Nueva York (UTC-4)", offset_hours=-4, size=250)
        self.clock_ny.pack(side=tk.LEFT, expand=True, padx=5)
        self.clock_tokyo = ClockWidget(clocks_frame, "Tokio (UTC+9)", offset_hours=9, size=250)
        self.clock_tokyo.pack(side=tk.LEFT, expand=True, padx=5)

        # Bottom frame con controles y historial
        bottom_frame = tk.Frame(self, bg=FRAME_BG)
        bottom_frame.pack(fill=tk.BOTH, expand=False, padx=20, pady=10)

        # Controles (izquierda)
        controls_frame = tk.Frame(bottom_frame, bg=FRAME_BG)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.add_alarm_btn = tk.Button(controls_frame, text="⏰ Alarma Personalizada",
                                        command=self.add_alarm_dialog, bg=BUTTON_BG, fg=BUTTON_FG,
                                        font=(FONT_FAMILY, 10, "bold"), cursor="hand2", width=22)
        self.add_alarm_btn.pack(pady=5)

        # Alarmas rápidas
        tk.Label(controls_frame, text="Alarmas Rápidas:", bg=FRAME_BG, fg=TEXT_COLOR,
                 font=(FONT_FAMILY, 10, "bold")).pack(pady=(10, 0))
        quick_frame = tk.Frame(controls_frame, bg=FRAME_BG)
        quick_frame.pack(pady=5)
        offsets = [("1m", 1), ("5m", 5), ("15m", 15), ("30m", 30)]
        for txt, mins in offsets:
            tk.Button(quick_frame, text=f"+{txt}", command=lambda m=mins: self.add_quick_alarm(m),
                      bg=BUTTON_BG, fg=BUTTON_FG, font=(FONT_FAMILY, 9), cursor="hand2", width=5).pack(side=tk.LEFT, padx=2)

        self.alarms_label = tk.Label(controls_frame, text="Alarmas activas: 0",
                                      bg=FRAME_BG, fg=TEXT_COLOR, font=(FONT_FAMILY, 12))
        self.alarms_label.pack(pady=5)

        # Historial (derecha)
        history_frame = tk.Frame(bottom_frame, bg=FRAME_BG)
        history_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(30, 10))
        history_lbl = tk.Label(history_frame, text="Historial de Alarmas (Log)",
                               bg=FRAME_BG, fg=TEXT_COLOR, font=(FONT_FAMILY, 11, "bold"))
        history_lbl.pack(anchor="w")
        self.history_listbox = tk.Listbox(history_frame, bg="#ffffff", fg=TEXT_COLOR,
                                          font=("Consolas", 10), height=6, relief=tk.FLAT,
                                          selectbackground=ACCENT_COLOR)
        self.history_listbox.pack(fill=tk.BOTH, expand=True, pady=5)

        self.update_clocks()

    def add_alarm_dialog(self):
        dlg = CustomAlarmDialog(self)
        self.wait_window(dlg)
        if dlg.result:
            h, m, msg, rep = dlg.result
            self.alarm_manager.add_alarm(h, m, msg, rep)
            self.update_alarms_label()
            rep_msg = f"se repetirá cada {rep} min" if rep > 0 else "se repetirá diariamente"
            messagebox.showinfo("Alarma Creada", f"Programada para {h:02d}:{m:02d}\n{rep_msg}", parent=self)

    def add_quick_alarm(self, minutes):
        future = datetime.now() + time.timedelta(minutes=minutes)
        h, m = future.hour, future.minute
        self.alarm_manager.add_alarm(h, m, f"Recordatorio (+{minutes}m)", 0)
        self.update_alarms_label()
        messagebox.showinfo("Alarma Rápida", f"Programada para {h:02d}:{m:02d}", parent=self)

    def update_alarms_label(self):
        active = len([a for a in self.alarm_manager.alarms if a.enabled])
        self.alarms_label.config(text=f"Alarmas activas: {active}")

    def refresh_history(self):
        self.history_listbox.delete(0, tk.END)
        for log in reversed(self.alarm_manager.history):
            self.history_listbox.insert(tk.END, f"  {log}")

    def update_clocks(self):
        l_h, l_m, _ = self.clock_local.update_clock()
        self.clock_ny.update_clock()
        self.clock_tokyo.update_clock()
        triggered = self.alarm_manager.check_alarms(l_h, l_m)
        for alarm in triggered:
            self.trigger_alarm(alarm)
            self.refresh_history()
        self.after(200, self.update_clocks)

    def trigger_alarm(self, alarm):
        def play():
            try:
                for _ in range(5):
                    winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
                    time.sleep(0.2)
            except Exception:
                pass
        threading.Thread(target=play, daemon=True).start()
        # Flash background
        original = self.cget("bg")
        def flash(cnt):
            if cnt:
                new_bg = ACCENT_COLOR if self.cget("bg") == original else original
                self.configure(bg=new_bg)
                self.after(300, flash, cnt-1)
            else:
                self.configure(bg=original)
                messagebox.showinfo("¡Alarma Disparada!",
                                    f"⏰ Hora: {alarm.hour:02d}:{alarm.minute:02d}\nMensaje: {alarm.message}",
                                    parent=self)
                self.update_alarms_label()
        flash(6)

if __name__ == "__main__":
    app = ClockApp()
    app.mainloop()
