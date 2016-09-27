class HealthStatus(object):
    def __init__(self, is_up = False):
        self.is_up = is_up

    def to_dict(self):
        return self.__dict__

class ServerTime(object):
    def __init__(self, hour = 0, minute = 0, second = 0, tz_name = 'Default', tz_offset = 0):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.tz_name = tz_name
        self.tz_offset = tz_offset

    def to_dict(self):
        return self.__dict__
