import npyscreen


class SelectHosts(npyscreen.ActionForm):
    def create(self):
        self.select_hosts_title = self.add(npyscreen.TitleText, name="Please select host(s):", value="", editable=False, begin_entry_at=70, )
        self.select_hosts_options = self.add(npyscreen.MultiSelect, max_height=4, value=[1, 2],
                 values=["Host1", "Host2", "Host3"], scroll_exit=True, width=20)

    def on_ok(self):
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.on_ok()
