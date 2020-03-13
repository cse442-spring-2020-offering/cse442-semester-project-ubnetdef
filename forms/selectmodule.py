import npyscreen
from overrides.constants import *
import overrides.shared_variables as sv

class SelectModule(npyscreen.ActionForm):
    def create(self):
        self.select_group_title = self.add(npyscreen.TitleText, name="Please select one of the availiable modules",                                   value="", editable=False, begin_entry_at=70, )
        self.method = sv.HOSTS_CONFIG[sv.SELECTIONS[0]]['method']
        modules = sv.method_to_module_map[self.method]
        self.group_selected = self.add(npyscreen.SelectOne, max_height=4, values=modules, scroll_exit=True, width=30)

    def on_ok(self):
        sv.METHOD = self.method
        sv.MODULE = self.group_selected.get_selected_objects()[0]
        self.parentApp.getForm('MAIN').reload_screen()
        self.parentApp.switchFormPrevious()


    def on_cancel(self):
        self.parentApp.switchFormPrevious()
