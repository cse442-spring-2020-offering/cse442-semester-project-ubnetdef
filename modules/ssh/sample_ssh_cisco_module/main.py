from modules.ssh.ssh import ConnectionSSH
class SampleModule(ConnectionSSH):
    def run(self):
        self.command('mkdir test')
        self.command('echo test created!')
        self.upload_file("test_file.txt", "test_file.txt")