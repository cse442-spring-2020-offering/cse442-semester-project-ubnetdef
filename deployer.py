import overrides.override_add_std
import npyscreen
from overrides.constants import *
from forms.mainform import MainForm
from forms.hosts_forms.addhosts import AddHosts
from forms.placeholderform import PlaceHolderForm
from forms.hosts_forms.addgroup import AddGroup
from forms.hosts_forms.selecthosts import SelectHosts
from forms.hosts_forms.selectgroup import SelectGroup



class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainForm)
        self.addForm(ADD_HOSTS, AddHosts)
        self.addForm(ADD_GROUP, AddGroup)
        self.addForm(SELECTED_HOSTS, SelectHosts)
        self.addForm(SELECTED_GROUP, SelectGroup)
        self.addForm(PLACEHOLDER_FORM, PlaceHolderForm)


def main():
    TA = App()
    TA.run()

if __name__ == '__main__':
    main()