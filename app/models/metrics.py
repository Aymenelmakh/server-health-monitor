from datetime import datetime
import copy
from app.models.cpu_metrics import CpuMetrics
from app.models.memory_metrics import MemoryMetrics
from app.models.disk_metrics import DiskMetrics
from app.models.network_metrics import NetworkMetrics
from app.models.system_metrics import SystemMetrics
from app.models.process_metrics import ProcessMetrics
from app.models.sensor_metrics import SensorMetrics
from app.models.security_metrics import SecurityMetrics
from app.models.health_status import HealthStatus

class Metrics:
    # CPU thresholds
    CPU_WARNING = 75
    CPU_CRITICAL = 90

    # RAM thresholds
    RAM_WARNING = 75
    RAM_CRITICAL = 90

    # Disk thresholds
    DISK_WARNING = 85
    DISK_CRITICAL = 95


    cpu:CpuMetrics
    memory : MemoryMetrics
    disk : DiskMetrics
    network : NetworkMetrics
    system : SystemMetrics
    process : ProcessMetrics
    sensor : SensorMetrics
    security : SecurityMetrics
    timestamp: datetime | None

    def __init__(self):
        self.cpu = CpuMetrics()
        self.memory = MemoryMetrics()
        self.disk = DiskMetrics()
        self.network = NetworkMetrics()
        self.system = SystemMetrics()
        self.process = ProcessMetrics()
        self.sensor = SensorMetrics()
        self.security = SecurityMetrics()

        self.timestamp = None

    def to_dict(self):
        return {
            "cpu":self.cpu.to_dict(),
            "ram":self.memory.to_dict(),
            "disk":self.disk.to_dict(),
            "network":self.network.to_dict(),
            "system":self.system.to_dict(),
            "process": self.process.to_dict(),
            "sensor":self.sensor.to_dict(),
            "security":self.security.to_dict(),
            "timestamp" : self.timestamp.isoformat() if self.timestamp else None
        }

    def __str__(self):
        return (
            f"Metrics(\n"
            f"  CPU:\n{self.cpu}\n\n"
            f"  Memory:\n{self.memory}\n\n"
            f"  Disk:\n{self.disk}\n\n"
            f"  Network:\n{self.network}\n\n"
            f"  System:\n{self.system}\n\n"
            f"  Processes:\n{self.process}\n\n"
            f"  Sensors:\n{self.sensor}\n\n"
            f"  Security:\n{self.security}\n\n"
            f"  Timestamp: {self.timestamp}\n"
            f")"
        )

    def update_timestamp(self):
        self.timestamp = datetime.now()

    def is_complete(self):
        return (
            self.cpu.is_complete() 
            and self.memory.is_complete()
            and self.disk.is_complete()
            and self.network.is_complete()
            and self.system.is_complete()
            and self.process.is_complete()
            and self.sensor.is_complete()
            and self.security.is_complete()
            and self.timestamp is not None
    )

    def clear(self):
        self.__init__()

    def copy(self):
        return copy.deepcopy(self)

    def health_status(self):
        # Metrics not collected yet
        if (
            self.cpu.cpu_percent is None or
            self.memory.ram_stats is None or
            not self.disk.disk_usage
        ):
            return HealthStatus.UNKNOWN

        cpu = self.cpu.cpu_percent
        ram = self.memory.ram_stats["percent"]

        # Highest disk usage among all partitions
        disk = max(
            usage["percent"]
            for usage in self.disk.disk_usage.values()
        )
        # Critical
        if (
        cpu >= self.CPU_CRITICAL or
        ram >= self.RAM_CRITICAL or
        disk >= self.DISK_CRITICAL
        ):
            return HealthStatus.CRITICAL
        # Warning
        if (
            cpu >= self.CPU_WARNING or
            ram >= self.RAM_WARNING or
            disk >= self.DISK_WARNING
        ):
            return HealthStatus.WARNING
        return HealthStatus.HEALTHY

    @classmethod
    def from_dict(cls, metrics):
        obj = cls()

        obj.cpu = CpuMetrics.from_dict(metrics.get("cpu"))
        obj.memory = MemoryMetrics.from_dict(metrics.get("ram"))
        obj.disk = DiskMetrics.from_dict(metrics.get("disk"))
        obj.network = NetworkMetrics.from_dict(metrics.get("network"))
        obj.system = SystemMetrics.from_dict(metrics.get("system"))
        obj.process = ProcessMetrics.from_dict(metrics.get("process"))
        obj.sensor = SensorMetrics.from_dict(metrics.get("sensor"))
        obj.security = SecurityMetrics.from_dict(metrics.get("security"))
        obj.timestamp = (
            datetime.fromisoformat(metrics.get("timestamp"))
            if metrics.get("timestamp")
            else None
        )

        return obj