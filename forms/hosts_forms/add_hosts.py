import npyscreen
class add_hosts(npyscreen.ActionForm):
    def create(self):
        self.OK_BUTTON_TEXT = "Save"
        self.add(npyscreen.TitleText, name="Please fill in following information:", value="", editable=False, begin_entry_at=70,)
        self.add(npyscreen.TitleText, name="Comma separated resolvable hostname, or ip address.", value="X.X.X.X,", editable=True, begin_entry_at=70)
        self.add(npyscreen.TitleText, name="Username (Usually SSH/WINRM)", value="", editable=True, begin_entry_at=70)
        self.add(npyscreen.TitleText, name="Password (Usually SSH/WINRM)", value="", editable=True, begin_entry_at=70)
        self.add(npyscreen.TitleText, name="Additional Arguments could be added here using json format:", value="", editable=False, begin_entry_at=70)
        self.add(npyscreen.MultiLineEditableBoxed,
                        max_height=10,
                        name='Arguments in json format',
                        footer="Press i or o to insert values, esc to exit the form",
                        values=["{'test': 'test'}"],
                        slow_scroll=False,
                        wrap="True"
                 )
        #TODO: Fix Resizing Issue with multiple Screens

        # self.add(npyscreen.ButtonPress, name="Add Additional arguments")

    def on_ok(self):
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.on_ok()
