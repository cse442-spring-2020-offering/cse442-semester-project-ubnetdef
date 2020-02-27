import overrides.override_add_std
import npyscreen
from overrides.constants import *
from forms.mainform import MainForm


class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainForm)


if __name__ == '__main__':
    App().run()
