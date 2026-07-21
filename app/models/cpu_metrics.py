import copy

class CpuMetrics:
    cpu_times: tuple | None
    cpu_percent: float | None

    cpu_times_percpu:list
    cpu_percent_percpu:list


    cpu_count_physical: int | None
    cpu_count_logical: int | None

    cpu_stats: tuple | None

    cpu_freq: tuple | None             # current, min, max
    cpu_freq_percpu: list

    cpu_loadavg: tuple | None           # 1, 5, 15 minutes

    def __init__(self):
        self.cpu_times = None
        self.cpu_percent = None

        self.cpu_times_percpu = []
        self.cpu_percent_percpu = []


        self.cpu_count_physical = None
        self.cpu_count_logical = None

        self.cpu_stats = None

        self.cpu_freq = None
        self.cpu_freq_percpu = []

        self.cpu_loadavg = None

    def to_dict(self):
        return {
            "cpu_times": self.cpu_times,
            "cpu_percent": self.cpu_percent,
            "cpu_times_percpu": self.cpu_times_percpu,
            "cpu_percent_percpu": self.cpu_percent_percpu,
            "cpu_count_physical": self.cpu_count_physical,
            "cpu_count_logical": self.cpu_count_logical,
            "cpu_stats": self.cpu_stats,
            "cpu_freq": self.cpu_freq,
            "cpu_freq_percpu": self.cpu_freq_percpu,
            "cpu_loadavg": self.cpu_loadavg
        }
    
    def __str__(self):
        return (
            f"CpuMetrics(\n"
            f"CPU Usage={self.cpu_percent}%, "
            f"Physical CPUs={self.cpu_count_physical}, "
            f"Logical CPUs={self.cpu_count_logical}\n"
        )

    def clear(self):
        self.__init__()
    
    def is_complete(self):
        return all(value is not None and value != [] and value != {} for value in self.__dict__.values())

    def copy(self):
        return copy.deepcopy(self)
    
    @classmethod
    def from_dict(cls, metrics):
        obj = cls()

        obj.cpu_times = metrics.get("cpu_times")
        obj.cpu_percent = metrics.get("cpu_percent")
        obj.cpu_times_percpu = metrics.get("cpu_times_percpu", [])
        obj.cpu_percent_percpu = metrics.get("cpu_percent_percpu", [])
        obj.cpu_count_physical = metrics.get("cpu_count_physical")
        obj.cpu_count_logical = metrics.get("cpu_count_logical")
        obj.cpu_stats = metrics.get("cpu_stats")
        obj.cpu_freq = metrics.get("cpu_freq")
        obj.cpu_freq_percpu = metrics.get("cpu_freq_percpu", [])
        obj.cpu_loadavg = metrics.get("cpu_loadavg")
        return obj