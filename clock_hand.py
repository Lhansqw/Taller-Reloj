import math

class ClockHand:
    """Encapsula longitud, grosor, color y cálculo del punto final de cada manecilla."""
    def __init__(self, length, thickness, color):
        self.length = length
        self.thickness = thickness
        self.color = color

    def calculate_end_point(self, center_x, center_y, angle):
        # angle está en grados (0° es las 12 en punto)
        # Convertir a radianes y ajustar porque en matemáticas 0° es a las 3
        rad = math.radians(angle)
        end_x = center_x + self.length * math.sin(rad)
        end_y = center_y - self.length * math.cos(rad)
        return end_x, end_y
