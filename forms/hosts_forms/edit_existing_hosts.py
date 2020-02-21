import npyscreen
from overrides.constants import *
from .addgroup import AddGroup

class EditHosts(AddGroup):
    def create(self):
        super().create()
        groupName = self.add(npyscreen.TitleText, name="Group Name:", value="", editable=True,
                 begin_entry_at=70, )
