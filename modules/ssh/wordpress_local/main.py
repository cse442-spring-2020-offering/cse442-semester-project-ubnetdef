from modules.ssh.ssh import ConnectionSSH
import overrides.shared_variables as sv
import os
from jinja2 import Template
class WordpressModule(ConnectionSSH):
    def run(self):
        self.command('whoami', sudo=True)
        self.command('apt-get update -y', sudo=True)
        self.command('apt-get install apache2 php mariadb-server mariadb-client php-mysql -y', sudo=True)
        self.command('service mysql start', sudo=True)
        db_name, db_username, db_password = {}, {}, {}
        for host in self.executable_hosts:
            db_name[host] = sv.HOSTS_CONFIG[host].get('db_name', 'wordpress')
            db_username[host] = sv.HOSTS_CONFIG[host].get('db_username', 'wordpress')
            db_password[host] = sv.HOSTS_CONFIG[host].get('db_password', 'changeme')


        with open(os.path.join(self.file_dir,  'database_config.jinja2'), 'r') as f:
            tm = Template(f.read())

        local_file_prefix = 'database_config'
        for i, host in enumerate(self.executable_hosts):
            with open(os.path.join(self.file_dir,  f"{local_file_prefix}{i}"), 'w') as f:
                f.write(tm.render(db_username=db_username[host], db_name=db_name[host],
                                            db_password=db_password[host]))
        copy_args = [dict(zip(('local_file', 'remote_file',),
                              (f"{local_file_prefix}{i}",
                               local_file_prefix,)))
                     for i, _ in enumerate(self.executable_hosts)]
        self.upload_file('%(local_file)s', '%(remote_file)s',
                                     copy_args=copy_args)
        self.command(f"mysql -u root < {local_file_prefix}", sudo=True)


        self.command(f"rm {local_file_prefix}")
        self.command('wget https://wordpress.org/latest.tar.gz')
        self.command('tar -xvf latest.tar.gz')
        self.command('cp -R wordpress /var/www/html/', sudo=True)
        self.command('chown -R www-data:www-data /var/www/html/wordpress/', sudo=True)
        self.command('chmod -R 755 /var/www/html/wordpress/', sudo=True)
        self.command('mkdir /var/www/html/wordpress/wp-content/uploads', sudo=True)
        self.command('chown -R www-data:www-data /var/www/html/wordpress/wp-content/uploads/', sudo=True)
        self.command('curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar')
        self.command('chmod +x wp-cli.phar')
        self.command('mv wp-cli.phar /usr/local/bin/wp', sudo=True)
        permissions_cmd = [f"wp config create --dbname={db_name[host]} --dbuser={db_username[host]} --dbpass={db_password[host]} --locale=ro_RO --allow-root --path=/var/www/html/wordpress" for host in self.executable_hosts]
        self.command('%s', host_args=permissions_cmd, sudo=True)
        self.command('chown www-data /var/www/html/wordpress/wp-config.php', sudo=True)
        self.command('service apache2 restart', sudo=True)

        for i, host in enumerate(self.executable_hosts):
            try:
                os.remove(os.path.join(self.file_dir,  f"{local_file_prefix}{i}"))
            except:
                continue


