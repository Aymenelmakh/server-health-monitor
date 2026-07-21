import copy 

class ProcessMetrics:
    total_processes: int | None
    running_processes: int | None
    sleeping_processes: int | None
    stopped_processes: int | None
    zombie_processes: int | None
    top_cpu_processes: list
    top_memory_processes: list

    def __init(self):
        self.total_processes = None
        self.running_processes = None
        self.sleeping_processes = None
        self.stopped_processes = None
        self.zombie_processes = None
        self.top_cpu_processes = []
        self.top_memory_processes = []
    
    def to_dict(self):
        return {
            "total_processes": self.total_processes,
            "running_processes": self.running_processes,
            "sleeping_processes": self.sleeping_processes,
            "stopped_processes": self.stopped_processes,
            "zombie_processes": self.zombie_processes,
            "top_cpu_processes": self.top_cpu_processes,
            "top_memory_processes": self.top_memory_processes
        }

    def __str__(self):
        return (
            f"Running Processes={self.running_processes}, "
            f"Sleeping={self.sleeping_processes}, "
            f"Zombie={self.zombie_processes}\n"
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
        obj.total_processes = metrics.get("total_processes")
        obj.running_processes = metrics.get("running_processes")
        obj.sleeping_processes = metrics.get("sleeping_processes")
        obj.stopped_processes = metrics.get("stopped_processes")
        obj.zombie_processes = metrics.get("zombie_processes")
        obj.top_cpu_processes = metrics.get("top_cpu_processes", [])
        obj.top_memory_processes = metrics.get("top_memory_processes", [])
        return obj