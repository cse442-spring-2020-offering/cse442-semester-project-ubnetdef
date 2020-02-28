import npyscreen
import overrides.shared_variables as sv

from overrides.constants import *


class AddGroup(npyscreen.ActionForm):
    def create(self):
        self.OK_BUTTON_TEXT = SAVE_BUTTON_TEXT
        self.intro_text = self.add(npyscreen.TitleText, name="Please fill in following information:", value="", editable=False, begin_entry_at=70, )
        self.group_name = self.add(npyscreen.TitleText, name="Group Name", value="", editable=True, begin_entry_at=70)
        self.multi_host_select = self.add(npyscreen.MultiSelect, max_height=4, values=list(sv.HOSTS_CONFIG.keys()), scroll_exit=True, width=20)

    def on_ok(self):
        if self.group_name.value and self.multi_host_select.values:

            for host in self.multi_host_select.values:
                if sv.HOSTS_CONFIG[host]['method'] != sv.HOSTS_CONFIG[self.multi_host_select.values[0]]['method']:
                    npyscreen.notify_confirm("Hosts do not share common remoting method", wide=True, editw=1)
                    return


            if self.group_name.value in sv.GROUPS_CONFIG.keys():
                if not npyscreen.notify_yes_no(
                        f"Group {self.group_name.value} already exists, would you like to override?",
                        title="Already Exists", editw=1):
                    return
            sv.CHANGES_PENDING = True
            sv.GROUPS_CONFIG[self.group_name.value] = []
            for host in self.multi_host_select.values:
                sv.GROUPS_CONFIG[self.group_name.value].append(host)
            self.parentApp.switchFormPrevious()
        else:
            npyscreen.notify_confirm("Please Make sure you select at least one host and give your group a name.", wide=True, editw=1)

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
