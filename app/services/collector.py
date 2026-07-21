import json
from app.services.ssh import SSHService
from app.models.server import Server
from app.models.metrics import Metrics
from datetime import datetime

class CollectorService:
    monitor_path:str

    def __init__(self, monitor_path=None):
        self.monitor_path = monitor_path

    def collect(self, server:Server):
        ssh = SSHService(server)
        ssh.connect()
        if server.is_online():
            try:
                stdin, stdout, stderr = ssh.execute_python()

                error = stderr.read().decode().strip()
                if error:
                    raise RuntimeError(error)

                data = json.loads(stdout.read().decode().strip())
                metrics = Metrics.from_dict(data)
                server.set_metrics(metrics)
                return server
            except Exception as e:
                return None
            finally:
                ssh.disconnect()
    
    def collect_all_servers(self, servers: list[Server]):
        print(f"[{datetime.now()}] Collecting metrics...")
        servers_collection = {}

        for server in servers:
            try:
                updated_server = self.collect(server)
                servers_collection[server.name] = updated_server.to_dict()
            except Exception as e:
                print(f"Failed to collect metrics from '{server.name}': {e}")
        return servers_collection
