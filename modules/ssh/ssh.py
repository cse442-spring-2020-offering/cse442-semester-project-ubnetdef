from pssh.clients import ParallelSSHClient
import overrides.shared_variables as sv 

class ConnectionSSH():
    def __init__(self):
        host_config = {}
        for host in sv.SELECTIONS:
            host_config[host] = {}
            host_config[host]['user'] = sv.HOSTS_CONFIG[host]['user']
            host_config[host]['password'] = sv.HOSTS_CONFIG[host]['password']
            if sv.HOSTS_CONFIG[host].get('port'):
                host_config[host]['port'] = sv.HOSTS_CONFIG[host]['port']
        self.client = ParallelSSHClient(sv.SELECTIONS, host_config=host_config)

    def run(self):
        pass # This method is meant to be overridden

    def version_detection(self):
        output = self.client.run_command('uname')
        for host, host_output in output.items():
            for line in host_output.stdout:
                print(line)

    def handler(self):
        pass