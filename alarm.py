class Alarm:
    """Representa una alarma individual con su estado y lógica de coincidencia."""
    def __init__(self, hour, minute, message="¡Alarma!"):
        self.hour = hour
        self.minute = minute
        self.message = message
        self.triggered = False
        self.enabled = True

    def check_match(self, current_hour, current_minute):
        if self.enabled and not self.triggered:
            if current_hour == self.hour and current_minute == self.minute:
                return True
        elif current_hour != self.hour or current_minute != self.minute:
            # Reiniciar el estado de 'disparada' cuando pasa el minuto de la alarma
            self.triggered = False
        return False
