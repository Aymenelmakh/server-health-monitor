import copy

class MemoryMetrics:
    ram_stats: tuple | None             # virtual_memory()
    swap_stats: tuple | None           # swap_memory()

    def __init__(self):
        self.ram_stats = None
        self.swap_stats = None

    def to_dict(self):
        return {
            "ram_stats": self.ram_stats,
            "swap_stats": self.swap_stats
        }

    def clear(self):
        self.__init__()
    
    def __str__(self):
        return (
            f"RAM={self.ram_stats}\n"
            f"Swap={self.swap_stats}\n"
        )

    def is_complete(self):
        return all(value is not None and value != [] and value != {} for value in self.__dict__.values())
    
    def copy(self):
        return copy.deepcopy(self)

    @classmethod
    def from_dict(cls, metrics):
        obj = cls()
        obj.ram_stats = metrics.get("ram_stats")
        obj.swap_stats = metrics.get("swap_stats")
        return obj