import npyscreen
from overrides.constants import *
from .addgroup import AddGroup
from .selectgroup import SelectGroup


class EditGroup(AddGroup, SelectGroup):
    def create(self):
        SelectGroup.create(self)
        self.bn_confirm = self.add(npyscreen.ButtonPress, name="Confirm Host to edit", )
        self.bn_confirm.whenPressed = self.hide_selection_details
        AddGroup.create(self)
        self.bn_delete_group = self.add(npyscreen.ButtonPress, name="DELETE GROUP", )
        self.bn_delete_group.whenPressed = self.on_ok

        self.bn_delete_group.hidden = True
        self.intro_text.hidden = True
        self.group_name.hidden = True
        self.multi_host_select.hidden = True
        self.select_group_title = True


    def hide_selection_details(self):
        self.bn_confirm.hidden = True
        self.group_selected.hidden = True
        self.multi_host_select.hidden = True

        self.bn_delete_group.hidden = False
        self.intro_text.hidden = False
        self.select_group_title = False
        self.group_name.hidden = False
        self.multi_host_select.hidden = False
        self.DISPLAY()