import npyscreen
class add_group(npyscreen.ActionForm):
    def create(self):
        self.OK_BUTTON_TEXT = "Save"
        self.add(npyscreen.TitleText, name="Please fill in following information:", value="", editable=False, begin_entry_at=70,)
        self.add(npyscreen.TitleText, name="Group Name", value="", editable=True, begin_entry_at=70)
        self.add(npyscreen.MultiSelect, max_height=4, value = [1,],
                values = ["Host1","Host2","Host3"], scroll_exit=True, width=20)

    def on_ok(self):
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.on_ok()
