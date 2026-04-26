from alarm import Alarm
from datetime import datetime

class AlarmManager:
    """Gestiona la lista de alarmas (agregar, eliminar, verificar disparo)."""
    def __init__(self):
        self.alarms = []
        self.history = [] # Historial de alarmas disparadas

    def add_alarm(self, hour, minute, message, repeat_minutes=0):
        alarm = Alarm(hour, minute, message, repeat_minutes)
        self.alarms.append(alarm)
        return alarm

    def remove_alarm(self, alarm):
        if alarm in self.alarms:
            self.alarms.remove(alarm)

    def check_alarms(self, current_hour, current_minute):
        triggered_alarms = []
        for alarm in self.alarms:
            if alarm.check_match(current_hour, current_minute):
                alarm.triggered = True
                
                # Avanzar tiempo si es recurrente por minutos
                if alarm.repeat_minutes > 0:
                    alarm.advance_time()
                
                # Registrar en el historial
                now = datetime.now()
                log_entry = f"[{now.strftime('%H:%M:%S')}] {alarm.message} (Sonó a las {current_hour:02d}:{current_minute:02d})"
                self.history.append(log_entry)
                
                triggered_alarms.append(alarm)
        return triggered_alarms
