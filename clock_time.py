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
        return now.hour, now.minute, now.second, now.microsecond

    def calculate_angles(self, hour, minute, second, microsecond):
       
        second_fraction = second + (microsecond / 1_000_000)
        second_angle = second_fraction * 6
        
  
        minute_fraction = minute + (second_fraction / 60)
        minute_angle = minute_fraction * 6
        
     
        hour_angle = (hour % 12) * 30 + (minute_fraction * 0.5)
        
        return hour_angle, minute_angle, second_angle
