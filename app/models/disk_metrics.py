import copy

class DiskMetrics:
    partitions: list             # disk_partitions()
    disk_usage: dict             # {mount_point: disk_usage()}
    disk_io_stats: tuple | None         # disk_io_counters()
    disk_io_stats_perdisk: dict  # disk_io_counters(perdisk=True)

    def __init__(self):
        self.partitions = []
        self.disk_usage = {}
        self.disk_io_stats = None
        self.disk_io_stats_perdisk = {}
    
    def to_dict(self):
        return{
            "partitions": self.partitions,
            "disk_usage": self.disk_usage,
            "disk_io_stats": self.disk_io_stats,
            "disk_io_stats_perdisk": self.disk_io_stats_perdisk
        }

    def __str__(self):
        return(
            f"Disk Usage={self.disk_usage}\n"
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
        obj.partitions = metrics.get("partitions", [])
        obj.disk_usage = metrics.get("disk_usage", {})
        obj.disk_io_stats = metrics.get("disk_io_stats")
        obj.disk_io_stats_perdisk = metrics.get("disk_io_stats_perdisk", {})
        return obj