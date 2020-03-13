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
        version_detection_hosts = (host for host in sv.SELECTION if
                                   sv.HOSTS_CONFIG[host].get('version_detection', True))
        output = self.client.run_command('cat /etc/*release', host_args=version_detection_hosts)

    def handler(self):
        # self.version_detection()
        self.run()