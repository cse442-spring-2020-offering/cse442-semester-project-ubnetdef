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

    def command(self, command, *args, **kwargs):
        output = self.client.run_command(command, *args, **kwargs)
        with sv.lock:
            for host, host_output in output.items():
                ret_string = f"Command ran: {command}\n"
                ret_string += "Output:\n" + '\n'.join(filter(None, host_output.stdout))
                ret_string += f"\nStatus Code: {str(host_output.exit_code)}\n\n"
                if host in sv.UPDATE_STATUS:
                    sv.UPDATE_STATUS[host] += ret_string
                else:
                    sv.UPDATE_STATUS[host] = ret_string
        return output

    # def version_detection(self):
    #     version_detection_hosts = (host for host in sv.SELECTION if
    #                                sv.HOSTS_CONFIG[host].get('version_detection', True))
    #     output = self.command('cat /etc/*release', host_args=version_detection_hosts)


    def handler(self):
        # self.version_detection()
        self.run()