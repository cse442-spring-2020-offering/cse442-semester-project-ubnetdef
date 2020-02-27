import npyscreen
from overrides.constants import *

class SaveProfile(npyscreen.ActionForm):
    def create(self):
        self.OK_BUTTON_TEXT = SAVE_BUTTON_TEXT
        self.profile_name = self.add(npyscreen.TitleText, name="Provide a Name for your profile: ", value="", editable=True, begin_entry_at=70, )
        self.encrypt = self.add(npyscreen.Checkbox, name="Encrypt the profile?")
        self.encrypt.whenToggled = self.unhide_pass
        self.profile_password = self.add(npyscreen.TitlePassword, name="Password to encrypt the configuration files",
                                         value="", editable=True, begin_entry_at=70, )
        self.profile_password.hidden = True


    def unhide_pass(self):
        self.profile_password.hidden = not self.profile_password.hidden
        self.DISPLAY()


    def on_ok(self):
        self.parentApp.switchFormPrevious()


    def on_cancel(self):
        self.on_ok()