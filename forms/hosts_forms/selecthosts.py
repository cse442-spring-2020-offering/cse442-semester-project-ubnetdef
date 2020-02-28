import npyscreen
import overrides.shared_variables as sv
from overrides.constants import *


class SelectHosts(npyscreen.ActionForm):
    def create(self):
        self.select_hosts_title = self.add(npyscreen.TitleText, name="Please select host(s):", value="", editable=False, begin_entry_at=70, )
        self.select_hosts_options = self.add(npyscreen.MultiSelect, max_height=4,
                 values=list(sv.HOSTS_CONFIG.keys()), scroll_exit=True, width=20)
    def on_ok(self):
        if not self.select_hosts_options.values:
            npyscreen.notify_confirm("Please select At least One Host", wide=True, editw=1)
        else:
            for host in self.select_hosts_options.values:
                if sv.HOSTS_CONFIG[host]['method'] != sv.HOSTS_CONFIG[self.select_hosts_options.values[0]]['method']:
                    npyscreen.notify_confirm("Hosts do not share common remoting method", wide=True, editw=1)
                    return
            sv.SELECTIONS = []
            for host in self.select_hosts_options.values:
                sv.SELECTIONS.append(host)
            self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
