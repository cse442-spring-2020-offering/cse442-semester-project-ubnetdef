from modules.ssh.ssh import ConnectionSSH
class SampleModule(ConnectionSSH):
    def run(self):
        output = self.client.run_command('mkdir test')