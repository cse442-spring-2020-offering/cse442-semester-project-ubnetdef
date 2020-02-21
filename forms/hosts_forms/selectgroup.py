import npyscreen


class SelectGroup(npyscreen.ActionForm):


    def create(self):
        self.select_group_title = self.add(npyscreen.TitleText, name="Please select a group", value="", editable=False, begin_entry_at=70, )
        self.group_selected = self.add(npyscreen.SelectOne, max_height=4,
                 values=["Group1", "Group2", "Group3"], scroll_exit=True, width=30)

    def on_ok(self):
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.on_ok()
