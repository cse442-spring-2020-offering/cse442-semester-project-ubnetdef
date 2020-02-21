import npyscreen
from overrides.constants import *
from .addgroup import AddGroup
from .selectgroup import SelectGroup


class EditGroup(AddGroup, SelectGroup):
    def create(self):
        SelectGroup.create(self)
        self.bn = self.add(npyscreen.ButtonPress, name="Confirm Host to edit", )
        self.bn.whenPressed = self.hide_selection_details
        AddGroup.create(self)
        self.intro_text.hidden = True
        self.group_name.hidden = True
        self.multi_host_select.hidden = True
        self.select_group_title = True


    def hide_selection_details(self):
        self.bn.hidden = True
        self.group_selected.hidden = True
        self.multi_host_select.hidden = True
        self.intro_text.hidden = False
        self.select_group_title = False
        self.group_name.hidden = False
        self.multi_host_select.hidden = False
        self.DISPLAY()