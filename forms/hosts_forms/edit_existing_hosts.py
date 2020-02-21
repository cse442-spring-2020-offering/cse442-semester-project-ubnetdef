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
        self.select_hosts_title = True
        self.add_hosts_title.hidden = True
        self.add_hosts_title2.hidden= True
        self.add_hosts_title3.hidden= True
        self.add_hosts_title4.hidden= True
        self.add_hosts_password.hidden= True
        self.add_hosts_json.hidden=True

    def show_edit_delete_screen(self):
        self.confirmButton.hidden = True
        self.select_hosts_options = True

        self.deleteHosts.hidden = False
        self.select_hosts_title = False
        self.add_hosts_title.hidden = False
        self.add_hosts_title2.hidden= False
        self.add_hosts_title3.hidden= False
        self.add_hosts_title4.hidden= False
        self.add_hosts_password.hidden= False
        self.add_hosts_json.hidden= False
        self.DISPLAY()





        # groupName = self.add(npyscreen.TitleText, name="Group Name:", value="", editable=True,
        #          begin_entry_at=70, )
