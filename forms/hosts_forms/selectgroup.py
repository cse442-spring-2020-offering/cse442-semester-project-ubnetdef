import npyscreen
import overrides.shared_variables as sv
from overrides.constants import *

class SelectGroup(npyscreen.ActionForm):
    def create(self):
        self.select_group_title = self.add(npyscreen.TitleText, name="Please select a group", value="", editable=False, begin_entry_at=70, )
        self.group_selected = self.add(npyscreen.SelectOne, max_height=4,
                 values=list(sv.GROUPS_CONFIG.keys()), scroll_exit=True, width=30)

    def on_ok(self):
        if not self.group_selected.get_selected_objects():
            npyscreen.notify_confirm("Please select a group", wide=True, editw=1)
        else:
            sv.SELECTIONS = []
            for host in sv.GROUPS_CONFIG[self.group_selected.get_selected_objects()[0]]:
                sv.SELECTIONS.append(host)
            self.parentApp.getForm('MAIN').reload_screen()
            self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
