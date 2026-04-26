import tkinter as tk
from tkinter import messagebox, simpledialog
import winsound
import time
import threading

from alarm_manager import AlarmManager
from clock_widget import ClockWidget

class ClockApp(tk.Tk):
    """Frontend Tkinter: orquesta los relojes, el historial y las alarmas."""
    def __init__(self):
        super().__init__()
        self.title("Sistema de Relojes Analógicos")
        self.geometry("900x450")
        self.configure(bg="#2c3e50")
        self.resizable(False, False)
        
        self.alarm_manager = AlarmManager()
        
        # Top Frame para los 3 Relojes
        clocks_frame = tk.Frame(self, bg="#2c3e50")
        clocks_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.clock_local = ClockWidget(clocks_frame, "Hora Local", offset_hours=None, size=250)
        self.clock_local.pack(side=tk.LEFT, expand=True)
        
        self.clock_ny = ClockWidget(clocks_frame, "Nueva York (UTC-4)", offset_hours=-4, size=250)
        self.clock_ny.pack(side=tk.LEFT, expand=True)
        
        self.clock_tokyo = ClockWidget(clocks_frame, "Tokio (UTC+9)", offset_hours=9, size=250)
        self.clock_tokyo.pack(side=tk.LEFT, expand=True)
        
        # Bottom Frame para Controles e Historial
        bottom_frame = tk.Frame(self, bg="#2c3e50")
        bottom_frame.pack(fill=tk.BOTH, expand=False, padx=20, pady=10)
        
        # Controles (Izquierda)
        controls_frame = tk.Frame(bottom_frame, bg="#2c3e50")
        controls_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.add_alarm_btn = tk.Button(controls_frame, text="+ Añadir Alarma", command=self.add_alarm_dialog, bg="#27ae60", fg="white", font=("Arial", 12, "bold"), cursor="hand2")
        self.add_alarm_btn.pack(pady=10)
        
        self.alarms_label = tk.Label(controls_frame, text="Alarmas activas: 0", bg="#2c3e50", fg="white", font=("Arial", 12))
        self.alarms_label.pack(pady=5)
        
        # Historial (Derecha)
        history_frame = tk.Frame(bottom_frame, bg="#2c3e50")
        history_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(50, 0))
        
        history_lbl = tk.Label(history_frame, text="Historial de Alarmas (Log)", bg="#2c3e50", fg="white", font=("Arial", 11, "bold"))
        history_lbl.pack(anchor="w")
        
        self.history_listbox = tk.Listbox(history_frame, bg="#34495e", fg="white", font=("Consolas", 10), height=5, relief=tk.FLAT, selectbackground="#1abc9c")
        self.history_listbox.pack(fill=tk.BOTH, expand=True)
        
        self.update_clocks()

    def add_alarm_dialog(self):
        time_str = simpledialog.askstring("Añadir Alarma", "Ingrese la hora (HH:MM) en formato 24h\n(Reloj Local):", parent=self)
        if time_str:
            try:
                hour, minute = map(int, time_str.split(":"))
                if 0 <= hour <= 23 and 0 <= minute <= 59:
                    message = simpledialog.askstring("Mensaje", "Mensaje de la alarma:", parent=self)
                    rep_str = simpledialog.askstring("Repetición", "Repetir cada N minutos (0 para que sea sólo diaria):", initialvalue="0", parent=self)
                    
                    try:
                        repeat_minutes = int(rep_str) if rep_str else 0
                    except ValueError:
                        repeat_minutes = 0
                        
                    self.alarm_manager.add_alarm(hour, minute, message or "¡Alarma!", repeat_minutes)
                    self.update_alarms_label()
                    
                    rep_msg = f"se repetirá cada {repeat_minutes} min" if repeat_minutes > 0 else "se repetirá diariamente"
                    messagebox.showinfo("Alarma Creada", f"Programada para {hour:02d}:{minute:02d} y {rep_msg}", parent=self)
                else:
                    messagebox.showerror("Error", "Hora inválida.")
            except ValueError:
                messagebox.showerror("Error", "Formato inválido. Use HH:MM.")

    def update_alarms_label(self):
        active_alarms = len([a for a in self.alarm_manager.alarms if a.enabled])
        self.alarms_label.config(text=f"Alarmas activas: {active_alarms}")

    def refresh_history(self):
        self.history_listbox.delete(0, tk.END)
        # Mostrar las alarmas más recientes primero
        for log in reversed(self.alarm_manager.history):
            self.history_listbox.insert(tk.END, f"  {log}")

    def update_clocks(self):
        # Actualizar la hora en los 3 relojes
        l_h, l_m, l_s = self.clock_local.update_clock()
        self.clock_ny.update_clock()
        self.clock_tokyo.update_clock()
        
        # Verificar alarmas según la hora local
        triggered = self.alarm_manager.check_alarms(l_h, l_m)
        for alarm in triggered:
            self.trigger_alarm(alarm)
            self.refresh_history()
            
        self.after(100, self.update_clocks)

    def trigger_alarm(self, alarm):
        def play_sound():
            try:
                for _ in range(3):
                    winsound.Beep(800, 300)
                    time.sleep(0.1)
                    winsound.Beep(1000, 500)
                    time.sleep(0.2)
            except Exception:
                pass
        
        original_bg = self.cget("bg")
        
        def flash_colors(count):
            if count > 0:
                current_bg = self.cget("bg")
                next_bg = "#e74c3c" if current_bg == original_bg else original_bg
                self.configure(bg=next_bg)
                self.after(300, flash_colors, count-1)
            else:
                self.configure(bg=original_bg)
                # Al terminar de parpadear, mostramos la alerta visual final
                messagebox.showinfo("¡Alarma Disparada!", f"⏰ Hora: {alarm.hour:02d}:{alarm.minute:02d}\nMensaje: {alarm.message}", parent=self)
                self.update_alarms_label()
        
        threading.Thread(target=play_sound, daemon=True).start()
        flash_colors(10)
