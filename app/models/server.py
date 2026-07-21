from app.models.metrics import Metrics
import os

class Server:
    id:int
    name:str
    host:str
    port:int
    username:str
    private_key:str
    metrics:Metrics | None
    OS:str
    status:str

    def __init__(self, id, name, host, port, username, private_key, OS, status, metrics : Metrics | None = None):
        self.id = id
        self.name = name
        self.host = host
        self.port = port
        self.username = username
        self._private_key = private_key
        self.metrics = metrics
        self.OS = OS
        self._status = status
    
    @property
    def private_key(self):
        return self._private_key

    @property
    def status(self):
        return self._status
    
    def to_dict(self):
        return {
            "id":self.id, 
            "name":self.name,
            "host":self.host,
            "port":self.port,
            "username":self.username,
            "private_key":self.private_key,
            "metrics": self.metrics.to_dict() if self.metrics else None,
            "OS":self.OS,
            "status":self.status
            }
    
    def set_status(self, stat):
        if stat not in ("ONLINE", "OFFLINE", "UNKNOWN"):
            raise ValueError(f"Invalid status: {stat}")
        self._status = stat
    
    def __str__(self):
        return f"Server(id={self.id}, name={self.name}, host={self.host}, port={self.port}, username={self.username}, os={self.OS}, status={self.status})"

    def is_online(self):
        return self.status == "ONLINE"

    def set_metrics(self, metrics: Metrics):
        self.metrics = metrics

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["name"],
            data["host"],
            data["port"],
            data["username"],
            os.getenv(data["private_key"]),
            data["OS"],
            data["status"]
        )