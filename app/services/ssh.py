import paramiko
from app.models.server import Server
from paramiko.ssh_exception import SSHException
import logging
import os

logging.getLogger("paramiko").disabled = True
logging.getLogger("paramiko.transport").disabled = True

class SSHService:
    server:Server
    client:paramiko.SSHClient

    def __init__(self, server:Server):
        self.server = server
        self.client = paramiko.SSHClient()
    
    def connect(self):
        try:
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                hostname=self.server.host,
                username=self.server.username,
                key_filename=self.server.private_key,
                look_for_keys=False,
                allow_agent=False,
                timeout=5,          # TCP connection timeout
                auth_timeout=5,     # authentication negotiation timeout
                banner_timeout=5    # SSH banner exchange timeout
            )
            self.server.set_status("ONLINE")
        except SSHException:
            print(f"Authentication failed for server '{self.server.name}'")
            self.server.set_status("UNKNOWN")
        except Exception as e:
            print(f"Server '{self.server.name}' is unreachable")
            self.server.set_status("OFFLINE")

    def disconnect(self):
        self.client.close()

    def execute_python(self):
        return self.client.exec_command(f"python3 /home/{self.server.username}/metrics/monitor.py")

    def execute_command(self, cmd):
        return self.client.exec_command(cmd)

    def is_connected(self):
        if (self.server.status == "ONLINE"):
            return True
        return False

    def reboot(self):
        self.execute_command("sudo reboot")

    def upload_file(self, local_path:str, remote_path:str):
        sftp = self.client.open_sftp()
        try:
            remote_dir = os.path.dirname(remote_path)
            try:
                sftp.stat(remote_dir)
            except FileNotFoundError:
                sftp.mkdir(remote_dir)
            sftp.put(local_path, remote_path)
        finally:
            sftp.close()

    def download_file(self, remote_path:str, local_path:str):
        sftp = self.client.open_sftp()
        try:
            local_dir = os.path.dirname(local_path)
            if local_dir:
                try:
                    os.stat(local_dir)
                except FileNotFoundError:
                    os.makedirs(local_dir)
            sftp.get(remote_path, local_path)
        finally:
            sftp.close()
    
    def shutdown(self):
        self.execute_command("sudo shutdown -h now")

    def is_file_exist(self, file_path:str):
        sftp = self.client.open_sftp()
        try:
            sftp.stat(file_path)
            return True
        except FileNotFoundError:
            return False
        finally:
            sftp.close()

