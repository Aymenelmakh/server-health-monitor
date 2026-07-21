import copy

class NetworkMetrics:
    network_io: tuple | None            # net_io_counters()
    network_io_pernic: dict      # net_io_counters(pernic=True)
    network_connections: list    # net_connections()
    nic_addresses: dict          # net_if_addrs()
    nic_stats: dict              # net_if_stats()

    def __init(self):
        self.network_io = None
        self.network_io_pernic = {}
        self.network_connections = []
        self.nic_addresses = {}
        self.nic_stats = {}

    def to_dict(self):
        return {
            "network_io": self.network_io,
            "network_io_pernic": self.network_io_pernic,
            "network_connections": self.network_connections,
            "nic_addresses": self.nic_addresses,
            "nic_stats": self.nic_stats,
        }

    def __str__(self):
        return (
            f"Network IO={self.network_io}\n"
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
        obj.network_io = metrics.get("network_io")
        obj.network_io_pernic = metrics.get("network_io_pernic", {})
        obj.network_connections = metrics.get("network_connections", [])
        obj.nic_addresses = metrics.get("nic_addresses", {})
        obj.nic_stats = metrics.get("nic_stats", {})
        return obj