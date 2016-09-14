class HealthStatus(object):
    def __init__(self, is_up = False):
        self.is_up = is_up

    def to_dict(self):
        return self.__dict__