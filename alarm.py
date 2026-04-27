class Alarm:
    """Representa una alarma individual con su estado y lógica de coincidencia."""
    def __init__(self, hour, minute, message="¡Alarma!", repeat_minutes=0):
        self.hour = hour
        self.minute = minute
        self.message = message
        self.repeat_minutes = repeat_minutes
        self.triggered = False
        self.enabled = True

    def check_match(self, current_hour, current_minute):
        if self.enabled and not self.triggered:
            if current_hour == self.hour and current_minute == self.minute:
                return True
        elif current_hour != self.hour or current_minute != self.minute:
            self.triggered = False
        return False
        
    def advance_time(self):
        """Avanza la alarma si tiene configuración de recurrencia en minutos."""
        if self.repeat_minutes > 0:
            total_minutes = self.minute + self.repeat_minutes
            added_hours = total_minutes // 60
            self.minute = total_minutes % 60
            self.hour = (self.hour + added_hours) % 24
