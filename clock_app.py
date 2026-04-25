import math
import time
import tkinter as tk
from tkinter import messagebox, simpledialog
import winsound
import threading

from clock_hand import ClockHand
from clock_time import ClockTime
from alarm_manager import AlarmManager

class ClockApp(tk.Tk):
    """Frontend Tkinter: dibuja el reloj analógico en Canvas y orquesta todo."""
    def __init__(self):
        super().__init__()
        self.title("Reloj Analógico")
        self.geometry("500x600")
        self.configure(bg="#2c3e50")
        self.resizable(False, False)
        
        self.clock_time = ClockTime()
        self.alarm_manager = AlarmManager()
        
        self.canvas_size = 400
        self.center = self.canvas_size // 2
        
        # Título
        title_lbl = tk.Label(self, text="Reloj Analógico con Alarmas", bg="#2c3e50", fg="white", font=("Helvetica", 16, "bold"))
        title_lbl.pack(pady=10)
        
        # Canvas para dibujar el reloj
        self.canvas = tk.Canvas(self, width=self.canvas_size, height=self.canvas_size, bg="#34495e", highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Instanciar las manecillas
        self.hour_hand = ClockHand(100, 6, "#ecf0f1")
        self.minute_hand = ClockHand(140, 4, "#bdc3c7")
        self.second_hand = ClockHand(160, 2, "#e74c3c")
        
        # Controles de la UI
        control_frame = tk.Frame(self, bg="#2c3e50")
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.add_alarm_btn = tk.Button(control_frame, text="+ Añadir Alarma", command=self.add_alarm_dialog, bg="#27ae60", fg="white", font=("Arial", 12, "bold"), cursor="hand2")
        self.add_alarm_btn.pack(side=tk.LEFT, padx=10)
        
        self.alarms_label = tk.Label(control_frame, text="Alarmas activas: 0", bg="#2c3e50", fg="white", font=("Arial", 12))
        self.alarms_label.pack(side=tk.RIGHT, padx=10)
        
        # Iniciar loop del reloj
        self.update_clock()

    def add_alarm_dialog(self):
        time_str = simpledialog.askstring("Añadir Alarma", "Ingrese la hora (HH:MM) en formato 24h:", parent=self)
        if time_str:
            try:
                hour, minute = map(int, time_str.split(":"))
                if 0 <= hour <= 23 and 0 <= minute <= 59:
                    message = simpledialog.askstring("Mensaje", "Ingrese un mensaje para la alarma:", parent=self)
                    self.alarm_manager.add_alarm(hour, minute, message or "¡Es hora!")
                    self.update_alarms_label()
                    messagebox.showinfo("Éxito", f"Alarma configurada para las {hour:02d}:{minute:02d}", parent=self)
                else:
                    messagebox.showerror("Error", "Hora inválida. Verifique que los valores estén en rango (0-23 y 0-59).")
            except ValueError:
                messagebox.showerror("Error", "Formato inválido. Use el formato HH:MM (ej. 14:30).")

    def update_alarms_label(self):
        active_alarms = len([a for a in self.alarm_manager.alarms if a.enabled])
        self.alarms_label.config(text=f"Alarmas activas: {active_alarms}")

    def draw_clock_face(self):
        self.canvas.delete("all")
        
        # Círculo principal del reloj
        self.canvas.create_oval(10, 10, self.canvas_size-10, self.canvas_size-10, outline="#2c3e50", width=4, fill="#1abc9c")
        self.canvas.create_oval(20, 20, self.canvas_size-20, self.canvas_size-20, outline="#16a085", width=2)
        
        # Dibujar marcas de las horas y minutos
        for i in range(60):
            angle = i * 6
            rad = math.radians(angle)
            
            # Si es una marca de hora (cada 5 minutos)
            if i % 5 == 0:
                start_x = self.center + 165 * math.sin(rad)
                start_y = self.center - 165 * math.cos(rad)
                end_x = self.center + 185 * math.sin(rad)
                end_y = self.center - 185 * math.cos(rad)
                self.canvas.create_line(start_x, start_y, end_x, end_y, fill="#ecf0f1", width=3)
                
                # Números (opcional, para que se vea más profesional)
                num = i // 5
                if num == 0: num = 12
                text_x = self.center + 145 * math.sin(rad)
                text_y = self.center - 145 * math.cos(rad)
                self.canvas.create_text(text_x, text_y, text=str(num), fill="#ecf0f1", font=("Helvetica", 14, "bold"))
            else:
                # Marca de minuto
                start_x = self.center + 175 * math.sin(rad)
                start_y = self.center - 175 * math.cos(rad)
                end_x = self.center + 185 * math.sin(rad)
                end_y = self.center - 185 * math.cos(rad)
                self.canvas.create_line(start_x, start_y, end_x, end_y, fill="#bdc3c7", width=1)

    def draw_hand(self, hand, angle):
        end_x, end_y = hand.calculate_end_point(self.center, self.center, angle)
        self.canvas.create_line(self.center, self.center, end_x, end_y, fill=hand.color, width=hand.thickness, capstyle=tk.ROUND)

    def update_clock(self):
        # Obtener lógica pura
        hour, minute, second = self.clock_time.get_current_time()
        hour_angle, minute_angle, second_angle = self.clock_time.calculate_angles(hour, minute, second)
        
        # Redibujar
        self.draw_clock_face()
        self.draw_hand(self.hour_hand, hour_angle)
        self.draw_hand(self.minute_hand, minute_angle)
        self.draw_hand(self.second_hand, second_angle)
        
        # Eje central de las manecillas
        self.canvas.create_oval(self.center-8, self.center-8, self.center+8, self.center+8, fill="#ecf0f1", outline="#2c3e50", width=2)
        
        # Revisar si se dispara alguna alarma
        triggered = self.alarm_manager.check_alarms(hour, minute)
        for alarm in triggered:
            self.trigger_alarm(alarm)
        
        # Programar la siguiente actualización
        self.after(100, self.update_clock)  # A 100ms para que se vea más fluido y se dispare a tiempo

    def trigger_alarm(self, alarm):
        # Efecto de sonido (Windows)
        def play_sound():
            try:
                for _ in range(3):
                    winsound.Beep(800, 300)
                    time.sleep(0.1)
                    winsound.Beep(1000, 500)
                    time.sleep(0.2)
            except Exception:
                pass
        
        # Notificación visual
        original_bg = self.cget("bg")
        
        def flash_colors(count):
            if count > 0:
                current_bg = self.cget("bg")
                next_bg = "#e74c3c" if current_bg == original_bg else original_bg
                self.configure(bg=next_bg)
                self.canvas.configure(bg="#c0392b" if next_bg == "#e74c3c" else "#34495e")
                self.after(300, flash_colors, count-1)
            else:
                self.configure(bg=original_bg)
                self.canvas.configure(bg="#34495e")
                messagebox.showinfo("¡Alarma Disparada!", f"⏰ Hora: {alarm.hour:02d}:{alarm.minute:02d}\nMensaje: {alarm.message}", parent=self)
                self.update_alarms_label()
        
        threading.Thread(target=play_sound, daemon=True).start()
        flash_colors(10)
