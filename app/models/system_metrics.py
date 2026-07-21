import copy

class SystemMetrics:
    hostname: str | None
    os_name: str | None
    os_version: str | None
    kernel_version: str | None
    architecture: str | None
    boot_time: float | None
    uptime: float | None
    logged_users: list

    def __init__(self):
        self.hostname = None
        self.os_name = None
        self.os_version = None
        self.kernel_version = None
        self.architecture = None
        self.boot_time = None
        self.uptime = None
        self.logged_users = []

    def to_dict(self):
        return {
            "hostname": self.hostname,
            "os_name": self.os_name,
            "os_version": self.os_version,
            "kernel_version": self.kernel_version,
            "architecture": self.architecture,
            "boot_time": self.boot_time,
            "uptime": self.uptime,
            "logged_users": self.logged_users
        }

    def __str__(self):
        return (
            f"Hostname={self.hostname}, "
            f"OS={self.os_name} {self.os_version}\n"
            f"Uptime={self.uptime}\n"
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
        obj.hostname = metrics.get("hostname")
        obj.os_name = metrics.get("os_name")
        obj.os_version = metrics.get("os_version")
        obj.kernel_version = metrics.get("kernel_version")
        obj.architecture = metrics.get("architecture")
        obj.boot_time = metrics.get("boot_time")
        obj.uptime = metrics.get("uptime")
        obj.logged_users = metrics.get("logged_users", [])
        return obj