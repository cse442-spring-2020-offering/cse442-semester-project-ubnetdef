import npyscreen
from overrides.constants import *
from .addhosts import AddHosts
from .selecthosts import SelectHosts

class EditHosts(AddHosts, SelectHosts):
    def create(self):
        SelectHosts.create(self)
        self.confirmButton = self.add(npyscreen.ButtonPress, name="Confirm Host to edit", value= "", )
        self.confirmButton.whenPressed = self.show_edit_delete_screen
        AddHosts.create(self)
        self.deleteHosts = self.add(npyscreen.ButtonPress, name="DELETE HOSTS", )
        self.deleteHosts.whenPressed = self.on_ok

        self.deleteHosts.hidden = True
        self.add_hosts_title.hidden = True
        self.add_hosts_ip_addresses.hidden= True
        self.add_hosts_username.hidden= True
        self.add_hosts_optional_args_title.hidden= True
        self.add_hosts_password.hidden= True
        self.add_hosts_args.hidden=True

    def show_edit_delete_screen(self):
        self.confirmButton.hidden = True
        self.select_hosts_options.hidden = True
        self.select_hosts_title.hidden = True
        self.deleteHosts.hidden = False
        self.add_hosts_title.hidden = False
        self.add_hosts_ip_addresses.hidden= False
        self.add_hosts_username.hidden= False
        self.add_hosts_optional_args_title.hidden= False
        self.add_hosts_password.hidden= False
        self.add_hosts_args.hidden= False
        self.DISPLAY()