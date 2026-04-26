from datetime import datetime, timezone, timedelta

class ClockTime:
    """Lógica pura de tiempo: obtener hora actual y calcular ángulos."""
    def __init__(self, offset_hours=None):
        self.offset_hours = offset_hours

    def get_current_time(self):
        if self.offset_hours is not None:
            tz = timezone(timedelta(hours=self.offset_hours))
            now = datetime.now(tz)
        else:
            now = datetime.now()
        return now.hour, now.minute, now.second

    def calculate_angles(self, hour, minute, second):
        # Segundero: 360 grados / 60 segundos = 6 grados por segundo
        second_angle = second * 6
        
        # Minutero: 360 grados / 60 minutos = 6 grados por minuto + aporte de los segundos
        minute_angle = minute * 6 + second * 0.1
        
        # Horario: 360 grados / 12 horas = 30 grados por hora + aporte de los minutos
        hour_angle = (hour % 12) * 30 + minute * 0.5
        
        return hour_angle, minute_angle, second_angle
