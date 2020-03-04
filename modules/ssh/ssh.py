from pssh.clients import ParallelSSHClient
import overrides.shared_variables as HOSTS_CONFIG

class ConnectionSSH():
    def __init__(self, hosts):
        self.hosts = hosts

    def run(self):
        pass

    def version_detection(self):
        pass
        output = self.client.run_command('uname')
        for host, host_output in output.items():
            for line in host_output.stdout:
                print(line)