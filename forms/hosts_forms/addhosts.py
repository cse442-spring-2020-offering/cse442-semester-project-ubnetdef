import npyscreen
from overrides.constants import *
import overrides.shared_variables as sv

import re
class AddHosts(npyscreen.ActionForm):

    def while_editing(self):
        self.check_to_delete_hosts()
    def check_to_delete_hosts(self, *args, **keywords):
        remote_hosts = "".join(self.add_hosts_ip_addresses.value.split()).split(',')
        if all(host in list(sv.HOSTS_CONFIG.keys()) for host in remote_hosts if host):
            self.deleteHosts.hidden = False
        else:
            self.deleteHosts.hidden = True
        self.DISPLAY()

    def delete_host(self):
        remote_hosts = "".join(self.add_hosts_ip_addresses.value.split()).split(',')
        for host in remote_hosts:
            if host:
                del sv.HOSTS_CONFIG[host]
                if host in sv.SELECTIONS: sv.SELECTIONS.remove(host)
                for host_list in sv.GROUPS_CONFIG.values():
                    if host in host_list: host_list.remove(host)
        self.parentApp.getForm('MAIN').reload_screen()
        self.parentApp.switchFormPrevious()

        #TODO: Decide what to do if a group becomes empty after removing hosts


    def unhide_cred_field(self):
        self.add_hosts_username.hidden = not self.add_hosts_username.hidden
        self.add_hosts_password.hidden = not self.add_hosts_password.hidden
        self.DISPLAY()


    def bulk_host_popup(self):
        file= npyscreen.selectFile()
        try:
            with open(file, 'r') as f:
                content = f.read()
                content = content.replace('\r\n', '\n')
                from detect_delimiter import detect
                delimiter = detect(content, whitelist=['\n', ','])
                ip_addresses = content.split(delimiter)
                current_value = self.add_hosts_ip_addresses.get_value()
                self.add_hosts_ip_addresses.set_value(f"{current_value}{',' if current_value[-1] != ',' else ''}{','.join(filter(None, ip_addresses))}")

        except FileNotFoundError:
            npyscreen.notify_confirm("File was not found!", title="Information Missing/Incorrect", wide=True, editw=1)
        except PermissionError:
            npyscreen.notify_confirm("You do not have permissions to open this file!", title="Information Missing/Incorrect", wide=True, editw=1)
        except UnicodeDecodeError:
            npyscreen.notify_confirm("We are unable to open the file. Make sure the file is human readable", title="Information Missing/Incorrect", wide=True, editw=1)
        except Exception as e:
            npyscreen.notify_confirm(f"Something went wrong, please retry, or select a different file.\nStack Trace:\n:{str(e)}",
                                     title="Equivalent of a 500 error", wide=True, editw=1)
        self.DISPLAY()
    def create(self):
        self.OK_BUTTON_TEXT = SAVE_BUTTON_TEXT
        self.add_hosts_title = self.add(npyscreen.TitleText, name="Please fill in following information:", value="", editable=False, begin_entry_at=70,)
        self.add_hosts_ip_addresses = self.add(npyscreen.TitleText, name="Comma separated resolvable hostname, or ip address.", value="X.X.X.X,", editable=True, begin_entry_at=70)
        self.bulk_hosts_addition = self.add(npyscreen.ButtonPress, name="Add hosts from comma/newline separated file of hosts")
        self.bulk_hosts_addition.whenPressed = self.bulk_host_popup
        self.add_hosts_title = self.add(npyscreen.TitleText, name="Please select one of the availiable configuration methods:", value="",
                                        editable=False, begin_entry_at=70, )
        self.select_hosts_method = self.add(npyscreen.SelectOne, max_height=4, values=sv.list_of_method_names, scroll_exit=True, width=20)
        self.winrm_or_ssh = self.add(npyscreen.Checkbox, name="requires credentials?")
        self.winrm_or_ssh.whenToggled = self.unhide_cred_field
        self.add_hosts_username = self.add(npyscreen.TitleText, name="Username", value="", editable=True, begin_entry_at=70)
        self.add_hosts_password = self.add(npyscreen.TitlePassword, name="Password", value="", editable=True, begin_entry_at=70)

        self.add_hosts_username.hidden = True
        self.add_hosts_password.hidden = True

        self.add_hosts_optional_args_title = self.add(npyscreen.TitleText, name="Optional arguments could be added here using json format:", value="", editable=False, begin_entry_at=70)
        self.add_hosts_args= self.add(npyscreen.MultiLineEditableBoxed,
                                      max_height=10,
                                      name='Optional Arguments in json format',
                                      footer="Press i or o to insert values, esc to exit the form",
                                      slow_scroll=True,
                                      wrap="True"
                                      )
        self.deleteHosts = self.add(npyscreen.ButtonPress, name="DELETE HOST(S)", )
        self.deleteHosts.whenPressed = self.delete_host
        self.deleteHosts.hidden = True
        self.check_to_delete_hosts()

        #TODO: Fix Resizing Issue with multiple Screens

        # self.add(npyscreen.ButtonPress, name="Add Additional arguments")

    @staticmethod
    def is_valid_ip_address(ip):
        import socket
        try:
            socket.inet_pton(socket.AF_INET, ip)
            return True
        except socket.error:
            try:
                socket.inet_pton(socket.AF_INET6, ip)
                return True
            except socket.error:
                pass
        return False

    @staticmethod
    def is_valid_hostname(hostname):
        if len(hostname) > 255:
            return False
        if hostname[-1] == ".":
            hostname = hostname[:-1]
        allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in hostname.split("."))


    def on_ok(self):
        remote_hosts = "".join(self.add_hosts_ip_addresses.value.split()).split(',')
        if not remote_hosts:
            npyscreen.notify_confirm(
                f"No values detected in Hosts Field", title="Information Missing/Incorrect", wide=True, editw=1)
            return

        if not self.add_hosts_username.hidden and not self.add_hosts_username.value:
            npyscreen.notify_confirm(
                f"Missing Value for Username", title="Information Missing/Incorrect", wide=True, editw=1)
            return

        if not self.add_hosts_password.hidden and not self.add_hosts_password.value:
            npyscreen.notify_confirm(
                f"Missing Value for Password", title="Information Missing/Incorrect", wide=True, editw=1)
            return

        if not self.select_hosts_method.hidden and not self.select_hosts_method.value:
            npyscreen.notify_confirm(
                f"Missing Value for Remoting Method", title="Information Missing/Incorrect", wide=True, editw=1)
            return

        args = None

        if self.add_hosts_args.get_values():
            import json
            import ast
            try:
                args = ast.literal_eval(''.join(self.add_hosts_args.get_values()))
            except SyntaxError:
                try:
                    args = json.loads(''.join(self.add_hosts_args.get_values()))
                except json.JSONDecodeError:
                    npyscreen.notify_confirm(
                        f"Failed to load additional arguments. Ensure the formatting is correct",
                        title="Information Missing/Incorrect", wide=True, editw=1)
                    return
        for address in [x for x in remote_hosts if x]:
            if not (self.is_valid_hostname(address) or self.is_valid_ip_address(address)):
                npyscreen.notify_confirm(
                    f"Following entry: {address} is not a valid hostname or IP address",
                    title="Information Missing/Incorrect", wide=True, editw=1)
                return
            if sv.HOSTS_CONFIG.get(address):
                if not npyscreen.notify_yes_no(
                    f"Host {address} already exists, would you like to override?",
                    title="Already Exists", editw=1):
                    return
            #TODO switch to ini format with configparser

        sv.CHANGES_PENDING = True
        for address in remote_hosts:
            if address:
                sv.HOSTS_CONFIG[address] = {}
                sv.HOSTS_CONFIG[address]['method'] = self.select_hosts_method.get_selected_objects()[0]
                if not self.add_hosts_username.hidden:
                    sv.HOSTS_CONFIG[address]['user'] = self.add_hosts_username.value
                    sv.HOSTS_CONFIG[address]['pass'] = self.add_hosts_password.value
                if args:
                    for key, value in args.items():
                        sv.HOSTS_CONFIG[address][key] = value
        self.parentApp.getForm('MAIN').reload_screen()
        self.parentApp.switchFormPrevious()
    def on_cancel(self):
        self.parentApp.switchFormPrevious()
