import copy

class SecurityMetrics:
    ssh_service_running: bool | None
    firewall_enabled: bool | None
    fail2ban_enabled: bool | None
    open_ports: list
    failed_login_attempts: int | None

    def __init__(self):
        self.ssh_service_running = None
        self.firewall_enabled = None
        self.fail2ban_enabled = None
        self.open_ports = []
        self.failed_login_attempts = None

    def to_dict(self):
        return {
            "ssh_service_running": self.ssh_service_running,
            "firewall_enabled": self.firewall_enabled,
            "fail2ban_enabled": self.fail2ban_enabled,
            "open_ports": self.open_ports,
            "failed_login_attempts": self.failed_login_attempts
        }

    def __str__(self):
        return (
            f"Firewall Enabled={self.firewall_enabled}, "
            f"SSH Running={self.ssh_service_running}, "
            f"Fail2Ban Enabled={self.fail2ban_enabled}\n"
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
        obj.ssh_service_running = metrics.get("ssh_service_running")
        obj.firewall_enabled = metrics.get("firewall_enabled")
        obj.fail2ban_enabled = metrics.get("fail2ban_enabled")
        obj.open_ports = metrics.get("open_ports", [])
        obj.failed_login_attempts = metrics.get("failed_login_attempts")
        return obj