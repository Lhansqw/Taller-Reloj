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

        second_angle = second * 6
        

        minute_angle = minute * 6 + second * 0.1
        

        hour_angle = (hour % 12) * 30 + minute * 0.5
        
        return hour_angle, minute_angle, second_angle
