import overrides.override_add_std
import npyscreen

from forms.main_form import main_form
from forms.hosts_forms.add_hosts import add_hosts
from forms.place_holder_form import place_holder_form

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", main_form)
        self.addForm("AddHosts", add_hosts)
        self.addForm("PlaceHolderForm", place_holder_form)

def main():
    TA = App()
    TA.run()

if __name__ == '__main__':
    main()