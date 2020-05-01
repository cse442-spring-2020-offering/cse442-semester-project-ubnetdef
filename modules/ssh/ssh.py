from pssh.clients import ParallelSSHClient
import overrides.shared_variables as sv
import os
import pathlib
from gevent import joinall
import json

class ConnectionSSH():

    VERSION = {}

    def generate_client(self, hosts):
        host_config = {}
        for host in hosts:
            host_config[host] = {}
            host_config[host]['user'] = sv.HOSTS_CONFIG[host]['user']
            host_config[host]['password'] = sv.HOSTS_CONFIG[host]['password']
            if sv.HOSTS_CONFIG[host].get('port'):
                host_config[host]['port'] = sv.HOSTS_CONFIG[host]['port']
        return ParallelSSHClient(hosts, host_config=host_config)

    def run(self):
        pass # This method is meant to be overridden

    def command(self, command, *args, **kwargs):
        output = self.client.run_command(command, *args, **kwargs)
        return self.logger(output, f"Command ran: {command}\n")

    def upload_file(self, file_name, remote_path, *args, **kwargs):
        path = pathlib.Path(__file__).parent.absolute()
        target_dir = os.path.join(path, sv.MODULE, 'files',  file_name)
        greenlets = self.client.copy_file(target_dir, remote_path, *args, **kwargs)

        joinall(greenlets, raise_error=True)

    def logger(self, output, comment = ''):
        with sv.lock:
            for host, host_output in output.items():
                ret_string = comment
                ret_string += "Output:\n" + '\n'.join(filter(None, host_output.stdout))
                ret_string += f"\nStatus Code: {str(host_output.exit_code)}\n\n"
                if host in sv.UPDATE_STATUS:
                    sv.UPDATE_STATUS[host] += ret_string
                else:
                    sv.UPDATE_STATUS[host] = ret_string
        return output

    def version_detection(self,version_detection_hosts):
        self.VERSION = {}
        version_detection_client = self.generate_client(version_detection_hosts)
        output = version_detection_client.run_command('cat /etc/*release')
        for host, host_output in output.items():
            os_dict = {}
            list_of_lines = filter(None, host_output.stdout)
            for line in list_of_lines:
                k, v = line.rstrip().split("=")
                os_dict[k] = v.strip('"')

            self.VERSION[host] = os_dict

    def handler(self):
        version_detection_hosts = [host for host in sv.SELECTIONS if
                                   sv.HOSTS_CONFIG[host].get('version_detection', True)]
        self.version_detection(version_detection_hosts)
        path = pathlib.Path(__file__).parent.absolute()
        target_dir = os.path.join(path, sv.MODULE, 'config.json')
        if os.path.exists(target_dir):
            with open(target_dir, 'r') as f:
                module_config = json.loads(f.read())
        else:
            module_config = {}
        unmatched_hosts = []
        constraints = module_config.get("constraints", {})
        for host, v in self.VERSION.items():
            match = 0
            for key, parameter in v.items():
                if key in constraints.keys() and parameter in constraints[key]:
                    match+=1
            if match != len(constraints.keys()):
                unmatched_hosts.append(host)

        with sv.lock:
            for host in unmatched_hosts:
                sv.UPDATE_STATUS[host] = f"The host did not match version detection.\nHost parameters are:{json.dumps(self.VERSION)}\nRequired parameters are:{json.dumps(constraints)}"

        executable_hosts = [host for host in sv.SELECTIONS if host not in unmatched_hosts]
        self.client = self.generate_client(executable_hosts)

        self.run()