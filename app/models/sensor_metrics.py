import copy

class SensorMetrics:
    temperatures: dict
    fans: dict
    battery: tuple | None

    def __init__(self):
        self.temperatures = {}
        self.fans = {}
        self.battery = None

    def to_dict(self):
        return {
            "temperatures": self.temperatures,
            "fans": self.fans,
            "battery": self.battery
        }

    def __str__(self):
        return (
            f"Temperatures={self.temperatures}\n"
        )
    
    def clear(self):
        self.__init__()

    def copy(self):
        return copy.deepcopy(self)
    
    def is_complete(self):
        return all(value is not None and value != [] and value != {} for value in self.__dict__.values())
    
    @classmethod
    def from_dict(cls, metrics):
        obj = cls()
        obj.temperatures = metrics.get("temperatures", {})
        obj.fans = metrics.get("fans", {})
        obj.battery = metrics.get("battery")

        return obj
