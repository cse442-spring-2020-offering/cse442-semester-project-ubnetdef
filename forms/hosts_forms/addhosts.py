import npyscreen
from overrides.constants import *
import overrides.shared_variables as sv

import re
class AddHosts(npyscreen.ActionForm):

    def unhide_cred_field(self):
        self.add_hosts_username.hidden = not self.add_hosts_username.hidden
        self.add_hosts_password.hidden = not self.add_hosts_password.hidden
        self.DISPLAY()

    def create(self):
        self.OK_BUTTON_TEXT = SAVE_BUTTON_TEXT
        self.add_hosts_title = self.add(npyscreen.TitleText, name="Please fill in following information:", value="", editable=False, begin_entry_at=70,)
        self.add_hosts_ip_addresses = self.add(npyscreen.TitleText, name="Comma separated resolvable hostname, or ip address.", value="X.X.X.X,", editable=True, begin_entry_at=70)
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
                                      values=[""],
                                      slow_scroll=True,
                                      wrap="True"
                                      )
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
        if self.add_hosts_args.value:
            import json
            try:
                args = json.loads(self.add_hosts_args.value)
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

        sv.CHANGES_PENDING = True
        for address in remote_hosts:
            if address:
                sv.HOSTS_CONFIG[address] = {}
                if not self.add_hosts_username.hidden:
                    sv.HOSTS_CONFIG[address]['username'] = self.add_hosts_username.value
                    sv.HOSTS_CONFIG[address]['password'] = self.add_hosts_password.value
                    sv.HOSTS_CONFIG[address]['method'] = self.select_hosts_method.values[0]
                if args:
                    sv.HOSTS_CONFIG[address]['args'] = args
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
