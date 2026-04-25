from alarm import Alarm

class AlarmManager:
    """Gestiona la lista de alarmas (agregar, eliminar, verificar disparo)."""
    def __init__(self):
        self.alarms = []

    def add_alarm(self, hour, minute, message):
        alarm = Alarm(hour, minute, message)
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
                triggered_alarms.append(alarm)
        return triggered_alarms
