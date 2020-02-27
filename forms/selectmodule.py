import npyscreen
from overrides.constants import *


class SelectModule(npyscreen.ActionForm):
    def create(self):
        self.select_group_title = self.add(npyscreen.TitleText, name="Please select one of the availiable modules",
                                           value="", editable=False, begin_entry_at=70, )
        self.group_selected = self.add(npyscreen.SelectOne, max_height=4, values=method_to_module_map[METHOD],
                                       scroll_exit=True, width=30)

    def on_ok(self):
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.on_ok()
