import math
import tkinter as tk
from clock_time import ClockTime
from clock_hand import ClockHand

class ClockWidget(tk.Frame):
    """Componente visual reutilizable para mostrar un reloj analógico."""
    def __init__(self, parent, title, offset_hours=None, size=200, *args, **kwargs):
        super().__init__(parent, bg="white", *args, **kwargs)
        
        self.size = size
        self.center = self.size // 2
        self.clock_time = ClockTime(offset_hours)
        
        
        self.title_lbl = tk.Label(self, text=title, bg="white", fg="#2c3e50", font=("Arial", 12, "bold"))
        self.title_lbl.pack(pady=5)
        

        self.canvas = tk.Canvas(self, width=self.size, height=self.size, bg="white", highlightthickness=0)
        self.canvas.pack()
        

        scale = size / 400
        self.hour_hand = ClockHand(100 * scale, max(2, int(6 * scale)), "#2c3e50")
        self.minute_hand = ClockHand(140 * scale, max(1, int(4 * scale)), "#7f8c8d")
        self.second_hand = ClockHand(160 * scale, max(1, int(2 * scale)), "#e74c3c")

    def draw_clock_face(self):
        self.canvas.delete("all")
        
      
        self.canvas.create_oval(10, 10, self.size-10, self.size-10, outline="#2c3e50", width=max(1, self.size//100), fill="white")
        self.canvas.create_oval(20, 20, self.size-20, self.size-20, outline="#bdc3c7", width=max(1, self.size//200))
        
        scale = self.size / 400
     
        for i in range(60):
            angle = i * 6
            rad = math.radians(angle)
            
            if i % 5 == 0:
                start_x = self.center + (165 * scale) * math.sin(rad)
                start_y = self.center - (165 * scale) * math.cos(rad)
                end_x = self.center + (185 * scale) * math.sin(rad)
                end_y = self.center - (185 * scale) * math.cos(rad)
                self.canvas.create_line(start_x, start_y, end_x, end_y, fill="#2c3e50", width=max(1, int(3*scale)))
                
                num = i // 5
                if num == 0: num = 12
                text_x = self.center + (140 * scale) * math.sin(rad)
                text_y = self.center - (140 * scale) * math.cos(rad)
                font_size = max(8, int(14 * scale))
                self.canvas.create_text(text_x, text_y, text=str(num), fill="#2c3e50", font=("Helvetica", font_size, "bold"))
            else:
                start_x = self.center + (175 * scale) * math.sin(rad)
                start_y = self.center - (175 * scale) * math.cos(rad)
                end_x = self.center + (185 * scale) * math.sin(rad)
                end_y = self.center - (185 * scale) * math.cos(rad)
                self.canvas.create_line(start_x, start_y, end_x, end_y, fill="#7f8c8d", width=1)

    def draw_hand(self, hand, angle):
        end_x, end_y = hand.calculate_end_point(self.center, self.center, angle)
        self.canvas.create_line(self.center, self.center, end_x, end_y, fill=hand.color, width=hand.thickness, capstyle=tk.ROUND)

    def update_clock(self):
        hour, minute, second = self.clock_time.get_current_time()
        hour_angle, minute_angle, second_angle = self.clock_time.calculate_angles(hour, minute, second)
        
        self.draw_clock_face()
        self.draw_hand(self.hour_hand, hour_angle)
        self.draw_hand(self.minute_hand, minute_angle)
        self.draw_hand(self.second_hand, second_angle)
        
        center_rad = max(2, int(8 * (self.size / 400)))
        self.canvas.create_oval(self.center-center_rad, self.center-center_rad, self.center+center_rad, self.center+center_rad, fill="#2c3e50", outline="#2c3e50", width=2)
        
        return hour, minute, second
