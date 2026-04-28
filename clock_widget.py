import math
import tkinter as tk
from clock_time import ClockTime
from clock_hand import ClockHand
from styles import *

class ClockWidget(tk.Frame):
    """Componente visual reutilizable para mostrar un reloj analógico."""
    def __init__(self, parent, title, offset_hours=None, size=200, *args, **kwargs):
        super().__init__(parent, bg=get_style("frame_bg"), *args, **kwargs)
        
        self.size = size
        self.center = self.size // 2
        self.clock_time = ClockTime(offset_hours)
        
        
        self.title_lbl = tk.Label(self, text=title, bg=get_style("frame_bg"), fg=get_style("text"), font=FONT_BOLD)
        self.title_lbl.pack(pady=5)
        

        self.canvas = tk.Canvas(self, width=self.size, height=self.size, bg=get_style("canvas_bg"), highlightthickness=0)
        self.canvas.pack()
        

        scale = size / 400
        self.hour_hand = ClockHand(100 * scale, max(2, int(6 * scale)), get_style("accent"))
        self.minute_hand = ClockHand(140 * scale, max(1, int(4 * scale)), get_style("secondary"))
        self.second_hand = ClockHand(160 * scale, max(1, int(2 * scale)), get_style("alert"))

    def update_styles(self):
        """Update colors when theme changes."""
        self.configure(bg=get_style("frame_bg"))
        self.title_lbl.configure(bg=get_style("frame_bg"), fg=get_style("text"))
        self.canvas.configure(bg=get_style("canvas_bg"))
        self.hour_hand.color = get_style("accent")
        self.minute_hand.color = get_style("secondary")
        self.second_hand.color = get_style("alert")

    def draw_clock_face(self):
        self.canvas.delete("all")
        
      
        self.canvas.create_oval(10, 10, self.size-10, self.size-10, outline=get_style("accent"), width=max(1, self.size//100), fill=get_style("canvas_bg"))
        self.canvas.create_oval(20, 20, self.size-20, self.size-20, outline=get_style("border"), width=max(1, self.size//200))
        
        scale = self.size / 400
     
        for i in range(60):
            angle = i * 6
            rad = math.radians(angle)
            
            if i % 5 == 0:
                start_x = self.center + (165 * scale) * math.sin(rad)
                start_y = self.center - (165 * scale) * math.cos(rad)
                end_x = self.center + (185 * scale) * math.sin(rad)
                end_y = self.center - (185 * scale) * math.cos(rad)
                self.canvas.create_line(start_x, start_y, end_x, end_y, fill=get_style("accent"), width=max(1, int(3*scale)))
                
                num = i // 5
                if num == 0: num = 12
                text_x = self.center + (140 * scale) * math.sin(rad)
                text_y = self.center - (140 * scale) * math.cos(rad)
                font_size = max(8, int(14 * scale))
                self.canvas.create_text(text_x, text_y, text=str(num), fill=get_style("accent"), font=FONT_CLOCK_NUMS)
            else:
                start_x = self.center + (175 * scale) * math.sin(rad)
                start_y = self.center - (175 * scale) * math.cos(rad)
                end_x = self.center + (185 * scale) * math.sin(rad)
                end_y = self.center - (185 * scale) * math.cos(rad)
                self.canvas.create_line(start_x, start_y, end_x, end_y, fill=get_style("secondary"), width=1)

    def draw_hand(self, hand, angle):
        end_x, end_y = hand.calculate_end_point(self.center, self.center, angle)
        self.canvas.create_line(self.center, self.center, end_x, end_y, fill=hand.color, width=hand.thickness, capstyle=tk.ROUND)

    def update_clock(self):
        hour, minute, second, micro = self.clock_time.get_current_time()
        hour_angle, minute_angle, second_angle = self.clock_time.calculate_angles(hour, minute, second, micro)
        
        self.draw_clock_face()
        self.draw_hand(self.hour_hand, hour_angle)
        self.draw_hand(self.minute_hand, minute_angle)
        self.draw_hand(self.second_hand, second_angle)
        
        center_rad = max(2, int(8 * (self.size / 400)))
        self.canvas.create_oval(self.center-center_rad, self.center-center_rad, self.center+center_rad, self.center+center_rad, fill=get_style("accent"), outline=get_style("accent"), width=2)
        
        return hour, minute, second

class StopwatchWidget(ClockWidget):
    """Componente visual que funciona como cronómetro analógico."""
    def __init__(self, parent, title, size=200, *args, **kwargs):
        super().__init__(parent, title, offset_hours=None, size=size, *args, **kwargs)
        # Inicializar en 0
        self.draw_stopwatch(0, 0, 0, 0)

    def draw_stopwatch(self, hours, minutes, seconds, micro):
        """Dibuja las manecillas basadas en el tiempo transcurrido."""
        h_angle, m_angle, s_angle = self.clock_time.calculate_angles(hours, minutes, seconds, micro)
        
        self.draw_clock_face()
        self.draw_hand(self.hour_hand, h_angle)
        self.draw_hand(self.minute_hand, m_angle)
        self.draw_hand(self.second_hand, s_angle)
        
        center_rad = max(2, int(8 * (self.size / 400)))
        self.canvas.create_oval(self.center-center_rad, self.center-center_rad, self.center+center_rad, self.center+center_rad, 
                                fill=get_style("accent"), outline=get_style("accent"), width=2)

    def update_clock(self):
        # Desactivar el update_clock heredado para que no use la hora actual
        pass
