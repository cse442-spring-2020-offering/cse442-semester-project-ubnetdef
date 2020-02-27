import npyscreen
from overrides.constants import *


class SelectProfile(npyscreen.ActionForm):
    def create(self):
        self.select_profile_title = self.add(npyscreen.TitleText, name="Please Select the profile to load", value="",
                                             editable=False, begin_entry_at=70, )
        self.group_selected = self.add(npyscreen.SelectOne, max_width=80, max_height=4, values=[
            f"{profile}{' (Encrypted)' if profiles_properties[profile].get('encrypted') else ''}" for profile in
            list_of_profile_names], scroll_exit=True, width=30)
        self.profile_password = self.add(npyscreen.TitlePassword,
                                         name="Password to deencrypt the configuration files. (Only required for Encrypted profiles)",
                                         value="", editable=True, begin_entry_at=70, )

    def on_ok(self):
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.on_ok()
